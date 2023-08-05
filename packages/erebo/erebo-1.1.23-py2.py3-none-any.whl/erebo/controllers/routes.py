#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Set
import erebo.settings.settings as settings
import erebo.core.utils as utils
from erebo.model.rediss import RedisWrapper

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"

class Routes(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, *args, **kwargs):
        pass

    def add_routes(self, ip: str, every_jump: int = 1) -> bool:
        ret = False
        try:
            # cnt = 1
            with RedisWrapper() as db:
                containers = db.get_containers()
            cnt = len(containers)
            ret_proc = utils.route_target(False)
            for container in containers:
                ret_proc = utils.to_route(ip, container['ip'], cnt, True, every_jump)
                if not ret_proc: 
                    raise ValueError
                with RedisWrapper() as db:
                    _ = db.add_to_route(ip=ip, container_ip=container['ip'],
                            position=cnt)
                cnt -= 1
            ret_proc = utils.route_target(True)
            if not ret_proc: 
                raise ValueError
            ret = True
        except Exception as e:
            print(e)
        return ret

    def del_routes(self, ip: str, every_jump: int = 1) -> bool:
        ret = False
        try:
            with RedisWrapper() as db:
                routes = db.get_to_route(ip=ip)
            for route in routes:
                ret_proc = utils.to_route(
                    ip, route['ip'], route['position'], False, every_jump)
                if not ret_proc: 
                    raise ValueError
                with RedisWrapper() as db:
                    _ = db.del_to_route(ip=ip, container_ip=route['ip'])
            ret = True
            if not ret_proc: 
                raise ValueError
        except Exception as e:
            print(e)
        return ret