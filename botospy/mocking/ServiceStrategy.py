#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
"""


class ServiceStrategy( object ):
    """
    """

    def __init__( self,
                  strict = 1,
                  reuse  = 0 ):
        """
        """

        self._strict = strict
        self._reuse  = reuse
        
        self._targets = {}

    def register( self, target, **kwargs ):
        """
        """

        if self._reuse >= 0:
            method_call = MethodCall( **kwargs )
            meta        = [self._reuse, method_call]
            service     = kwargs["service"]

            if service not in self._targets:
                self._targets[ service ] = [meta]
                return

            self._targets[ service ].append( meta )

    def is_mocked( self, target, **kwargs ):
        """
        """

        if not self._targets or not target:
            return False

        if target in self._targets:
            return True
        
        service_name, method_name = target.rsplit(".", 1)
        
        if service_name in self._targets:
            return True

        return False

    def match( self, target, **kwargs ):
        """
        """

        if not self._targets or not target:
            return None

        for service, meta in self._targets:
            method_call = meta[1]
            if target == method_call.service:
                meta[0] -= 1
                if meta[0] < 0:
                    self._targets[service] = self._targets[service][1:]
                    if not self._targets[service]:
                        del self._targets[service]
                return method_call

        service_name, method_name = target.rsplit(".", 1)

        for service, meta in self._targets:
            method_call = meta[1]
            if service_name == method_call.service:
                meta[0] -= 1
                if meta[0] < 0:
                    self._targets[service] = self._targets[service][1:]
                    if not self._targets[service]:
                        del self._targets[service]
                return method_call

        return None

if __name__ == '__main__':
    pass
