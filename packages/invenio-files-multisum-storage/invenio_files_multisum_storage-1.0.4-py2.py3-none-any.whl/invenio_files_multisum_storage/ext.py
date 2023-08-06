# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio Files Multi-Checksum Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for Invenio Files Multi-Checksum Storage."""

from __future__ import absolute_import, print_function

from . import config


class InvenioFilesMultiChecksumStorage(object):
    """Invenio Files Multi-Checksum Storage extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        pass
