# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_nginx.schemas.base import get_config

OPTIONS = """
upstream polyaxon {{
  server unix:{root}/web/polyaxon.sock;
}}

server {{
    include polyaxon/polyaxon.base.conf;
}}

include polyaxon/polyaxon.redirect.conf;
"""


def get_main_config(root=None):
    root = root or "/polyaxon"
    return get_config(options=OPTIONS,
                      indent=0,
                      root=root)
