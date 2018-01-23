#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Will ensure no mocking will take place, this is a placeholder
mocking strategy
"""


#--- Classes ---

class NoopStrategy( object ):
    """
    A noop strategy that does nothing and ensures no
    mocking
    """

    def __init__( self ):
        """
        """

        pass

    def register( self, target, method_call ):
        """
        """

        pass

    def unregister( self, target, method_call ):
        """
        """

        pass

    def is_mocked( self, **kwargs ):
        """
        """

        return False

    def match( self, **kwargs ):
        """
        """

        return None


if __name__ == '__main__':
    pass
