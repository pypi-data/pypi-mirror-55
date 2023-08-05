#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Set
from erebo.core.docker_project import DockerProject
from erebo.core.utils import ping_vpn


__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"


class CheckVpn(object):

    def __init__(self, *args, **kwargs):
        self.__docker_client = DockerProject()
        # return super().__init__(*args, **kwargs)

    def __get_containers_info(self, all: bool = False):
        return  [
            {
                "container": x,
                "name": x.name, 
                "status": x.status, 
                "ip_addrs": x.attrs['NetworkSettings']['IPAddress'],
                "ports": x.attrs['NetworkSettings']['Ports'],
                "port": list(x.attrs['NetworkSettings']['Ports'])[0].split('/')[0]
            } 
            for x in self.__docker_client.get_containers(False)]

    def test_status(self):
        ret = []
        list_containers = self.__get_containers_info()
        for container in list_containers:
            status = ping_vpn(container["ip_addrs"]+':'+container["port"])
            ret.append(
                {
                    "container": container['container'],
                    "status": status['code']
                })
        return ret
            
