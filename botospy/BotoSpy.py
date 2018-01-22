#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The main entrypoint for the BotoSpy framework. 
Intended to be used programatically and via a cli
"""


__version__ = "0.0.3"


#--- Imports ---

# Python Classes
from contextlib import ContextDecorator
import copy
import os
from unittest.mock import patch

# 3rd Party Libraries
import boto3

# Our Classes
from mocking.FifoStrategy import FifoStrategy
from mocking.NoopStrategy import NoopStrategy
from MethodCall import MethodCall


#--- Classes ---

class BotoSpy( ContextDecorator ):
    """
    Serves as the controller for all botospy functionality
    """

    #--- Magic Methods ---

    def __init__( self, targets = None, strategy = None ):
        """
        Constructor for the BotoSpy class
        """
        self.targets = targets or []
        
        if targets:
            if not isinstance( targets, list ):
                self.targets = [targets]

        self._calls   = []
        self._orig    = None
        self._patch   = None
        self._env     = None
        self._matcher = NoopStrategy()
        
        if strategy:
            self._matcher = strategy

    def __enter__( self ):
        """
        """

        return self.activate()

    def __exit__( self, type, value, traceback ):
        """
        """

        return self.deactivate()


    #--- Monitoring Methods ---

    def mock( self, target, **kwargs ):
        """"""
        self.watch( target )

        new_target = target
        if not isinstance( target, list ):
            new_target = [target]

        for item in new_target:

            #service_name, method_name = item.rsplit(".", 1)
            
            self._matcher.register( item, **kwargs )

        return self

    def watch( self, target ):
        """"""

        new_target = target
        if not isinstance( target, list ):
            new_target = [target]

        self.targets.extend( new_target )

        return self


    #--- Context Management Methods ---

    def activate( self ):
        """
        """

        if self._patch:
            return self

        # reset calls
        self._calls = []

        def wrapper( client, operation_name, kwargs ):
            _orig = self._orig

            this_target = "{0}.{1}".format( client.meta.service_model.service_name, operation_name )
            if this_target not in self.targets:
                return _orig( client, operation_name, kwargs )

            method_call         = MethodCall()
            method_call.service = this_target
            method_call.kwargs  = kwargs

            service_name, method_name = this_target.rsplit(".", 1)

            try:
                match = self._matcher.match( this_target, **kwargs )
                
                if match is not None:
                    method_call = match
                else:
                    method_call.result = _orig( client, operation_name, kwargs )

            except Exception as e:
                method_call.exception = e

            self._calls.append( method_call )

            if method_call.exception:
                raise method_call.exception

            return method_call.result

        self._env  = copy.deepcopy( os.environ )
        self._orig = botocore.client.BaseClient._make_api_call
        self._patch = patch( 'botocore.client.BaseClient._make_api_call', autospec = True )
        self._patch.start().side_effect = wrapper

        return self

    def deactivate( self ):
        """
        """

        if self._patch:
            self._patch.stop()
            self._patch = None

        if self._orig:
            botocore.client.BaseClient._make_api_call = self._orig
            self._orig = None

        if self._env:
            os.environ.clear()
            os.environ.update(self._env)
            self._env = None

        return self


def main():
    """
    Main entrypoint for the cli
    """

    target  = sys.argv[1]
    targets = target.split( "," )

    spy = BotoSpy( targets )
    spy.activate()

    sys.exit( 1 )


#--- Main ---

if __name__ == '__main__':
    main()
