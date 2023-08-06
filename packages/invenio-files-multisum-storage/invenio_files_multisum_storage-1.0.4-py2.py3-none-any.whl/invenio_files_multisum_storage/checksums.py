# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Checksum algorithms."""
from collections import OrderedDict


class MultiChecksum(object):
    """ Class for computing/verifying multiple hash algorithms """

    algos = OrderedDict()

    def __init__(self, algos: dict):
        """ Initialize class with supported algos """
        self.algos = algos

    def __call__(self, *args, **kwargs):
        """ Initialize individual algos and return self as message digest """
        for algo, m in self.algos.items():
            if callable(m):
                self.algos[algo] = m()

        return self

    def update(self, chunk):
        """ Update algos digests with chunk """
        for digest in self.algos.values():
            digest.update(chunk)

    def hexdigest(self):
        """ Return hexdigest of all algo digests combined """
        return ';'.join([d.hexdigest() for d in self.algos.values()])
