# -*- coding: utf-8 -*-
from .url import Url


def init_config():

    config = {
        'rejected_domains': [],
        'accepted_domains': [],
        'scan_limit': None,
        'recursive': True,
        'link_depth': 2,
        'text_len_thr': 300,
        'title_len_thr': 3,
        'hx_len_thr': 30,
        'conn_timeout': 3.5,
        'limit': None,
        'delay': True
    }

    return config
