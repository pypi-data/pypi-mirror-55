#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Set
from random import randrange
from time import sleep
from erebo.core.docker_project import DockerProject
from erebo.model.rediss import RedisWrapper
import erebo.settings.settings as settings
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

class UpContainer(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, *args, **kwargs):
        self._dc = DockerProject()

    def create_container(self, name: str, iso2: str = None) -> bool:
        ret = False
        utils.print_message('| {} | \tStep: Getting External IP'.format(name))
        external_ip = utils.get_external_ip(container_name=name)
        try:
            image = "tsari/openvpn"
            port = randrange(5000, 7999)
            local_port = '3128'
            utils.print_message('| {} | \tStep: Creating Container'.format(name))
            ports = dict({ "".join((str(local_port), '/tcp')): port})
            container = self._dc.container_run(
                image, 
                name,
                '',
                ['/opt/vpn:/opt/vpn:rw'],
                ['/dev/net/tun'],
                ['NET_ADMIN'],
                ['8.8.8.8','1.1.23.1'],
                True,
                True,
                True,
                True,
                {},
                [],
                ports)
            utils.print_message('| {} | \tStep: Starting VPN'.format(name))
            if container:
                cnt = self._dc.get_container(name)
                cnt_ip = cnt.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
                host_ip = utils.get_external_ip(container_name=name)
                with RedisWrapper() as db:
                    db.add_container(
                        container=container,
                        name=name, 
                        ip=cnt_ip,
                        host_ip=host_ip,
                        local_port=local_port,
                        remote_port=port)
            else:
                utils.print_message('| {} | \tStep: Creating container  Error: 1001'.format(name))
                self.destroy_container(name=name)
                return ret
            if self.__exec_cmd(name=name, iso2=iso2):
                utils.print_message('| {} | \tStep: Getting VPN External IP'.format(name))
                container = self._dc.get_container_info(name)
                vpn_external_ip = utils.get_vpn_external_ip(
                    container=container, external_ip=external_ip)
                utils.print_message('| {} | \tStep: Saving VPN External IP'.format(name))
                if vpn_external_ip:
                    with RedisWrapper() as db:
                        db.add_container_vp_ip(
                            container_name=name, value=vpn_external_ip)
                    ret = True
                else:
                    utils.print_message('| {} | Cant get external vpn ip'.format(name))
                    self.destroy_container(name=name)
            else:
                self.destroy_container(name=name)
        except Exception:
            pass
        finally:
            return ret

    def __exec_cmd(self, name: str, iso2: str = None) -> bool:
        ret = False
        try:
            utils.print_message('| {} | \tStep: Exec VPN'.format(name))
            _ = self._dc.exec_vpn(name, iso2)
            ret = True
        except Exception as e:
            print("run {}".format(utils.print_exception()))
            print(" {} | Error running VPN - Error:{}").format(name, e)
        return ret

    def destroy_container(self, name: str) -> bool:
        ret = False
        try:
            utils.print_message('| {} | \tStep: Destroying Container'.format(name))
            if self._dc.container_stop_remove(name):
                utils.print_message('| {} | \tStep: Deleting Data'.format(name))
                with RedisWrapper() as db:
                    utils.print_message('| {} | \tStep: Deleting Container'.format(name))
                    db.del_container(container_name=name)
                    utils.print_message('| {} | \tStep: Deleting VPN IP'.format(name))
                    db.del_container_vp_ip(container_name=name)
                    utils.print_message('| {} | \tStep: Getting AUTH File'.format(name))
                    # auth_file = db.get_container_auth(container_name=name)
                    utils.print_message('| {} | \tStep: Decresing AUTH'.format(name))
                    # vutils.decrease_auth(auth_file['vpn_name'], auth_file['auth_file'])
                    utils.print_message('| {} | \tStep: Deleting AUTH File'.format(name))
                    db.del_container_auth(container_name=name)
                ret = True
        except Exception as e:
            utils.print_message("| {} | Error destroying Container error:{}".format(
                name, e))
            # print("error")
        finally:
            return ret
        