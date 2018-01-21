#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
"""


class FifoStrategy( object ):
    """
    """

    def __init__( self,
                  strict = 1,
                  reuse  = 0 ):
        """
        """

        self._strict = strict
        self._reuse  = reuse
        
        self._targets = []

    def register( self, method_call ):
        """
        """

        meta = [self._reuse, method_call]
        self._targets.append( meta )

    def is_mocked( self, target, **kwargs ):
        """
        """

        if not self._targets:
            return False

        # order is important and a full check
        if self._strict == 0:

            _, method_call = self._targets[0]:
            if target == method_call.service:
                return True

            return False

        # order not important until find first service
        if self._strict == 1:
            for _, method_call in self._targets:
                if target == method_call.service:
                    return True
            return False

        for _, method_call in self._targets:
            if target == method_call.service:
                if kwargs == method_call.kwargs:
                    return True
                break

            return False

        return False

    def match( self, target, **kwargs ):
        """
        """

        if self._strict:
            for i, meta in enumerate( self._targets ):
                method_call = meta[1]
                if target == method_call.service:
                    if kwargs == method_call.kwargs:
                        meta[0] -= 1
                        if meta[0] < 0:
                            del self._targets[i]
                        return method_call
                    break
            return None

        for i, meta in enumerate( self._targets ):
            method_call = meta[1]
            if target == method_call.service:
                meta[0] -= 1
                if meta[0] < 0:
                    del self._targets[i]
                return method_call

        return None

if __name__ == '__main__':
    pass
