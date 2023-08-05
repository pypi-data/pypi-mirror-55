#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Set
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from erebo.dispachers.dispacher import Dispacher as ds

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"


class Controller(object):
    """Class Dispacher """

    def __init__(self):
        self.futures = []
        self.executor = ThreadPoolExecutor(max_workers=1)

    def main(self, msg: Dict):
        executor = self.executor
        task = msg['task']
        if task == 'create_container':
            self.futures.append(
                executor.submit(ds.create, **msg))
        elif task == 'destroy_container':
            self.futures.append(
                executor.submit(ds.destroy, **msg))
        elif task == 'add_routes':
            self.futures.append(
                executor.submit(ds.add_route, **msg))
        elif task == 'del_routes':
            self.futures.append(
                executor.submit(ds.del_route, **msg))
        elif task == 'restart_vpn':
            self.futures.append(
                executor.submit(ds.restart_vpn, **msg))
        elif task == 'restart_vpn_ip':
            self.futures.append(
                executor.submit(ds.restart_vpn_ip, **msg))
        else:
            print(task)