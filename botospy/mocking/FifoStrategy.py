#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
When deciding a mocking result this strategy performs a first in first out call to result order
"""


#--- Imports ---

# Our Libraries
from ..MethodCall import MethodCall
from NoopStrategy import NoopStrategy


#--- Classes ---

class FifoStrategy( NoopStrategy ):
    """
    A first in first out strategy for deciding mock
    boto3 api results. 
    """

    def __init__( self,
                  strict = True,
                  reuse  = 0 ):
        """
        """

        self._strict = strict
        self._reuse  = reuse
        
        self._targets = []

    def register( self, target, method_call ):
        """
        """

        if target and self._reuse >= 0:

            meta = [self._reuse, target, method_call]

            self._targets.append( meta )

    def unregister( self, target, method_call ):
        """
        """

        if target:
            for i, meta in enumerate( self._targets ):
                if meta[1] == target:
                    del self._targets[i]
                    return meta[2]

    def is_mocked( self, **kwargs ):
        """
        """

        target = kwargs["target"] if "target" in kwargs else kwargs["service"]

        if not target or not self._targets:
            return False

        _, target_found, method_call = self._targets[0]

        if target == target_found:
        
            if not self._strict:
                return True

            if kwargs == method_call.kwargs:
                return True

        return False

    def match( self, **kwargs ):
        """
        """

        target = kwargs["target"] if "target" in kwargs else kwargs["service"]

        if not target or not self._targets:
            return None

        meta         = self._targets[0]
        target_found = meta[1]
        method_call  = meta[2]
        result       = None

        if target == target_found:

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
