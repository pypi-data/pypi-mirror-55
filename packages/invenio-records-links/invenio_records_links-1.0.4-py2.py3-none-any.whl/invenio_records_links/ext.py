# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Mirek Simek.
#
# invenio-records-links is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""A generic links module for Invenio"""

from __future__ import absolute_import, print_function

from . import config


class RecordsLinks(object):
    """invenio-records-links extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-records-links'] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('INVENIO_RECORDS_LINKS_'):
                app.config.setdefault(k, getattr(config, k))
