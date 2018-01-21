#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The main entrypoint for the BotoSpy framework. 
Intended to be used programatically and via a cli
"""


class MethodCall( object ):
    """
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

        return str( self.__dict__ )


if __name__ == '__main__':
    pass
