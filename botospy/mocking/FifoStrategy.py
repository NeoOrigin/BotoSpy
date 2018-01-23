#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
"""


# Our Libraries
from ..MethodCall import MethodCall


class FifoStrategy( object ):
    """
    """

    def __init__( self,
                  strict = True,
                  reuse  = 0 ):
        """
        """

        self._strict = strict
        self._reuse  = reuse
        
        self._targets = []

    def register( self, target, **kwargs ):
        """
        """

        if self._reuse >= 0:
            method_call = MethodCall( **kwargs )
            meta = [self._reuse, method_call]

            self._targets.append( meta )

    def is_mocked( self, target, **kwargs ):
        """
        """

        if not target or not self._targets:
            return False

        _, method_call = self._targets[0]

        if target == method_call.service:
        
            if not self._strict:
                return True

            if kwargs == method_call.kwargs:
                return True

        return False

    def match( self, target, **kwargs ):
        """
        """

        if not target or not self._targets:
            return None

        meta        = self._targets[0]
        method_call = meta[1]
        result      = None

        if target == method_call.service:

            if not self._strict:
                result = method_call
            elif kwargs == method_call.kwargs:
                result = method_call

            if result:
                meta[0] -= 1
                if meta[0] < 0:
                    del self._targets[0]

        return result


if __name__ == '__main__':
    pass
