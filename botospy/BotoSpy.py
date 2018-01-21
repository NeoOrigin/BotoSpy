#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The main entrypoint for the BotoSpy framework. 
Intended to be used programatically and via a cli
"""


__version__ = "0.0.1"


#--- Imports ---

# Python Classes
from unittest.mock import patch

# 3rd Party Libraries
import boto3

# Our Classes
from mocking.FifoStrategy import FifoStrategy
from MethodCall import MethodCall


#--- Classes ---

class BotoSpy( object ):
    """
    Serves as the controller for all botospy functionality
    """


    #--- Magic Methods ---

    def __init__( self, targets = None ):
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
        self._matcher = None

    def __enter__( self ):
        """
        """

        return self.activate()

    def __exit__( self ):
        """
        """

        return self.deactivate()


    #--- Monitoring Methods ---

    def mock( self, target, **kwargs ):
        """"""
        self.watch( target )

        service_name, method_name = target.rsplit(".", 1)

        if service_name in self._mock_data:
            mocks = self._mock_data[ service_name ]

            if method_name not in mocks:
                mocks[ method_name ] = []

            mocks[ method_name ].append( kwargs )
            return self

        self._mock_data[ service_name ] = { method_name: [kwargs] }

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

        self._calls = []

        def wrapper( client, operation_name, kwargs ):
            _orig = self._orig

            this_target = "{0}.{1}".format( client, operation_name )
            if this_target not in self.targets:
                return _orig( client, operation_name, kwargs )

            if not self._matcher:
                self._matcher = FifoStrategy()

            method_call         = MethodCall()
            method_call.service = this_target
            method_call.kwargs  = kwargs

            service_name, method_name = this_target.rsplit(".", 1)

            try:
                if client in self._mock_data:
                    if operation_name in self._mock_data[ client ]:
                        if self._mock_data[ client ][ operation_name ]:
                            call_data = self._mock_data[ client ][ operation_name ]
                                self._mock_data[ client ][ operation_name ] = self._mock_data[ client ][ operation_name ][1:]
                            
                           

                method_call.result = _orig( client, operation_name, kwargs )
            except Exception as e:
                method_call.exception = e

            self._calls.append( method_call )

            if method_call.exception:
                raise method_call.exception

            return method_call.result

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
            botocore.client.BaseClient._make_api_call = self._orig

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
