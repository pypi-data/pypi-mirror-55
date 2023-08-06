# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Mirek Simek.
#
# invenio-records-links is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""A generic links module for Invenio"""

from __future__ import absolute_import, print_function

from .ext import RecordsLinks
from .version import __version__
from .serializers import LinkedObjectSerializerMixin

__all__ = ('__version__', 'RecordsLinks', 'LinkedObjectSerializerMixin')
