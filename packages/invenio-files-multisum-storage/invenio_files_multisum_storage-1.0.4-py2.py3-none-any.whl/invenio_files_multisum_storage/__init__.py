# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio Files Multi-Checksum Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""PyFS File Storage For Invenio with support for multiple checksum algos"""

from __future__ import absolute_import, print_function

from .ext import InvenioFilesMultiChecksumStorage
from .version import __version__

__all__ = ('__version__', 'InvenioFilesMultiChecksumStorage')
