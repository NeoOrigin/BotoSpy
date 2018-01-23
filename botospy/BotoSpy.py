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
import pprint
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

    def __init__( self, targets = None, strategy = None, trace = False ):
        """
        Constructor for the BotoSpy class
        """
        self.targets  = targets or []
        self.trace    = trace
        
        self._calls   = []
        self._orig    = None
        self._patch   = None
        self._env     = None
        self._matcher = NoopStrategy()
        
        if targets:
            if not isinstance( targets, list ):
                self.targets = [targets]

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
            if this_target not in self.targets and client.meta.service_model.service_name not in self.targets:
                return _orig( client, operation_name, kwargs )

            method_call         = MethodCall()
            method_call.service = this_target
            method_call.kwargs  = kwargs

            #service_name, method_name = this_target.rsplit(".", 1)

            try:
                match = self._matcher.match( this_target, **kwargs )
                
                if match is not None:
                    method_call = match
                else:
                    method_call.result = _orig( client, operation_name, kwargs )

            except Exception as e:
                method_call.exception = e

            self._calls.append( method_call )

            if self.trace:
                pprint.pprint( method_call )

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

    @property
    def calls(self):
        """
        """
        return self.get_calls()

    def get_calls( self, target = None ):
        """
        """
        if not target:
            return self._calls

        new_target = target
        if not isinstance( target, list ):
            new_target = [target]

        found = []
        for item in new_target:

            service_name, method_name = item.rsplit(".", 1)

            if method_name:
                temp = [method_call for method_call in self._calls if method_call.service == item]
                found.extend( temp )
                continue

            temp = [method_call for method_call in self._calls if method_call.service.rsplit(".", 1)[0] == service_name]
            found.extend( temp )

        return found

def main():
    """
    Main entrypoint for the cli
    """

    target  = sys.argv[1]
    targets = target.split( "," )

    import awscli

    rc = 1
    del sys.argv[1]
    
    trace   = False
    mocks   = []
    methods = []

    last_index = -1
    skip = 0
    num_args = len( sys.argv )

    for i, arg in enumerate( sys.argv ):

        if skip > 0:
            skip -= 1
            continue

        if arg == "::":
            last_index = i
            break

        if arg == "--trace" and num_args > i+1:
            trace = bool( sys.argv[i+1] )
            skip  = 1
            continue

        if arg == "--mock" and num_args > i+1:
            mocks.append( sys.argv[i+1] )
            skip = 1
            method_info = { "mocked": True, "service": sys.argv[i+1] }

            for j, name in enumerate( sys.argv[i+2:] ):

                if name == "--args":
                    skip += 1
                    if num_args > i+j+3:
                        skip += 1
                        method_info[ "kwargs" ] = sys.argv[i+j+3]
                    continue
                if name == "--result":
                    skip += 1
                    if num_args > i+j+3:
                        skip += 1
                        method_info["result"] = sys.argv[i+j+3]
                    continue
                if name == "--raise":
                    skip += 1
                    if num_args > i+j+3:
                        skip += 1
                        method_info["exception"] = sys.argv[i+j+3]
                    continue
                break

            methods.append( method_info )
            continue

    if last_index >=0:
        sys.argv = sys.argv[last_index+1:]
    
    with BotoSpy( targets, trace = trace ) as bs:

        for i, mock_data in enumerate( mocks ):
            if methods[i]:
                bs.mock( mock_data, **methods[i] )
                continue
             bs.watch( mock_data )

        rc = awscli.clidriver.main()

    sys.exit( rc )


#--- Main ---

if __name__ == '__main__':
    main()
