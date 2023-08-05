#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime
from erebo.model.rediss import RedisWrapper
from erebo.controllers.restart_vpn import RestartVpn
import erebo.core.utils as utils

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"

class DaemonFnc(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self):
        self.rvpn =  RestartVpn()

    def restart_vpn_time(self, time_seg: int):
        while True:
            sleep(time_seg)
            try:        
                with RedisWrapper() as db:
                    containers = db.get_containers()
                ret = False
                for container in containers:
                    container_name = container['name']
                    utils.print_message(
                        '| {} | Automatic restart VPN in container'.format(
                            container_name))
                    try:
                        ret = self.rvpn.run(container_name=container_name)
                    except Exception:
                        utils.print_message(
                            '| {} | Error running vpn Error'.format(
                                container_name))
                    if ret:
                        utils.print_message(
                            '| {} | Automatic restart VPN in done'.format(
                                container_name))
                    else:
                        utils.print_message(
                            '| {} | Cant\'n restart VPN in container'.format(
                                container_name))
            except Exception as e:
                print("restart_vpn_time {}".format(utils.print_exception()))