#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
"""


#--- Imports ---

# Our Libraries
from NoopStrategy import NoopStrategy


#--- Classes --

class ServiceStrategy( NoopStrategy ):
    """
    Mocks are looked up by service name and method, if 
    no equivakent method found then just service will 
    be looked up.  If multiple found then this will 
    follow a first in first out order
    """

    def __init__( self,
                  strict = 1,
                  reuse  = 0 ):
        """
        """

        self._strict = strict
        self._reuse  = reuse
        
        self._targets = {}

    def register( self, target, method_call ):
        """
        Registers a mock with this strategy.
        """

        # No point continuing if the targets wont
        # survive even one call
        if target and self._reuse >= 0:

            meta = [self._reuse, target, method_call]

            # Append, each service gets a placeholder
            if target not in self._targets:
                self._targets[ target ] = []

            self._targets[ target ].append( meta )

    def unregister( self, target, method_call ):
        """
        """

        if target:
            for name, meta in self._targets.items():
                if name == target:
                    del self._targets[name]
                    return meta[2]

    def is_mocked( self, **kwargs ):
        """
        """

        target = kwargs["target"] if "target" in kwargs else kwargs["service"]

        if not self._targets or not target:
            return False

        if self._strict:
            for service_name, meta in self._target.items():
                if target == service_name and meta[2].kwargs = kwargs:
                    return True

            for service_name, meta in self._target.items():
                if target == service_name.rsplit(".", 1)[0] and meta[2].kwargs = kwargs:
                    return True

            return False

        # Not strict

        if target in self._targets:
            return True
        
        service_name = target.rsplit(".", 1)[0]
        
        if service_name in self._targets:
            return True

        return False

    def match( self, **kwargs ):
        """
        """

        target = kwargs["target"] if "target" in kwargs else kwargs["service"]

        if not self._targets or not target:
            return None

        for service_name, meta in self._targets.items():

            method_call = meta[2]
            if target != method_call.service:
                continue

            meta[0] -= 1
            if meta[0] < 0:
                self._targets[service_name] = self._targets[service_name][1:]
                if not self._targets[service_name]:
                    del self._targets[service_name]
            return method_call

        service_name = target.rsplit(".", 1)[0]

        for service, meta in self._targets.items():

            method_call = meta[2]
            if service_name != method_call.service:
                continue

            meta[0] -= 1
            if meta[0] < 0:
                self._targets[service] = self._targets[service][1:]
                if not self._targets[service]:
                    del self._targets[service]
            return method_call

        return None


if __name__ == '__main__':
    pass
