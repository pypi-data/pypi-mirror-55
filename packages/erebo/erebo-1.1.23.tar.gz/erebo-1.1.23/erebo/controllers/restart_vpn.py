#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Set
from time import sleep
import os
import signal
from erebo.core.docker_project import DockerProject
from erebo.controllers.check_vpn import CheckVpn
from erebo.model.rediss import RedisWrapper
import erebo.core.utils as utils
import erebo.core.utils as utils
import erebo.core.vpn_utils as vutils

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"


class RestartVpn(object):

    def __init__(self, *args, **kwargs):
        self.__docker_client = DockerProject()
        self.external_ip = ''
        self.vpn_exgternal_ip = {}
        # return super().__init__(*args, **kwargs)

    def _kill(self, container_name: str, process_name) -> bool:
        ret = False
        try:
            process = self.__docker_client.get_container_process_per_name(
                container_name, process_name)
            pids = [x[1] for x in process]
            # is_kill = self.__docker_client.kill_process(
            #     pids=pids, container_name=container_name)
            is_kill = self.__docker_client.kill_process_sudo(
                pids=pids, container_name=container_name)
            ret = is_kill
        except Exception:
            print("_kill {}".format(utils.print_exception()))
        finally:
            return ret

    def _init_vpn(self, container_name:str, iso2:str = None) -> Dict:
        ret = {}
        self.external_ip = utils.get_external_ip(container_name=container_name)
        try:
            vpn = self.__docker_client.exec_vpn(container_name, iso2)
            container = self.__docker_client.get_container_info(container_name)
            self.vpn_exgternal_ip = utils.get_vpn_external_ip(
                    container=container, external_ip=self.external_ip)
            if self.vpn_exgternal_ip:
                ret = vpn
        except Exception:
            print("_init_vpn {}".format(utils.print_exception()))
        finally:
            return ret

    def run(self, container_name:str, iso2:str = None) -> bool:
        utils.print_message('| {} | \tStep: Restart VPN'.format(container_name))
        ret = False
        try:
            with RedisWrapper() as db:
                # get auth_file
                utils.print_message('| {} | \tStep: Getting AUTH File'.format(container_name))
                auth_file = db.get_container_auth(container_name=container_name)
                # kill vpn
                utils.print_message('| {} | \tStep: Killing VPN'.format(container_name))
                if self._kill(
                        container_name=container_name,
                        process_name='openvpn'):
                    # decrement used auth file
                    utils.print_message('| {} | \tStep: Decreseing AUTH'.format(container_name))
                    # delete vpn and auth row in redis
                    utils.print_message('| {} |\tStep: Deleting AUTH'.format(container_name))
                    if db.del_container_auth(
                            container_name=container_name):
                        # up vpn
                        utils.print_message('| {} | \tStep: Start VPN'.format(container_name))
                        vpn = self._init_vpn(container_name=container_name,  iso2=iso2)
                        if vpn:
                            # add vpn and auth row in redis
                            utils.print_message('| {} | \tStep: Adding AUTH'.format(container_name))
                            db.add_container_auth(
                                container_name=vpn['container_name'],
                                auth_file=vpn['auth_file'], 
                                vpn_name=vpn['vpn_name'],
                                vpn_file=vpn['vpn_file'])
                            utils.print_message('| {} | \tStep: Adding Container'.format(container_name))
                            db.add_container_vp_ip(
                                container_name=vpn['container_name'],
                                value=self.vpn_exgternal_ip)
                            ret = True
        except Exception:
            print("run {}".format(utils.print_exception()))
        finally:
            return ret