# -*- coding: utf-8 -*-

import json
import requests
import time

# predispongo una minitastiera, con un solo tastp
keyboard_base = json.dumps({'keyboard': [["Check updates"]],
                            'one_time_keyboard': False,
                            'resize_keyboard': True})


