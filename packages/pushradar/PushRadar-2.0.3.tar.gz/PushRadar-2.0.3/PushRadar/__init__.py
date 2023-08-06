# -*- coding: utf-8 -*-
"""
pushradar-python
================

:copyright: (c) 2019 PushRadar
:license: MIT, see LICENSE for more details
"""

from .PushRadar import PushRadar
from .PushRadarAPIClient import PushRadarAPIClient
from .PushRadarClassInstances import PushRadarClassInstances
from .PushRadarUtils import PushRadarUtils

__title__ = 'PushRadar'
__authors__ = 'PushRadar'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019 PushRadar. All rights reserved.'
__version__ = '1.8.1'
__version_info__ = tuple(int(i) for i in __version__.split('.'))

__all__ = ['PushRadar', 'PushRadarAPIClient', 'PushRadarClassInstances', 'PushRadarUtils']