#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Represents the inputs and outputs of a boto3 method call.
"""


#--- Imports ---

# Python Libraries
import pprint


#--- Classes ---

class MethodCall( object ):
    """
    Represents the inputs and outputs of a boto3 method call
    """

    def __init__( self,
                  mocked    = True,
                  service   = None,
                  kwargs    = None,
                  result    = None,
                  exception = None ):
        """
        """

        self.mocked    = Mocked
        self.service   = service
        self.kwargs    = kwargs
        self.result    = result
        self.exception = exception

    def __str__( self ):
        """
        """

        return pprint.pformat( self.__dict__ )


if __name__ == '__main__':
    pass
