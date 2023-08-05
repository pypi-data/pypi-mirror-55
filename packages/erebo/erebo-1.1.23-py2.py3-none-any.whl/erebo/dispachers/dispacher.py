#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Dict, Tuple, Set
import erebo.core.utils as utils
import erebo.settings.settings as settings
from erebo.controllers.up_container import UpContainer
from erebo.controllers.routes import Routes
from erebo.controllers.restart_vpn import RestartVpn
from erebo.model.rediss import RedisWrapper

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"


class Dispacher(object):
    """Class Dispacher """

    upc = UpContainer()
    route = Routes()
    rvpn =  RestartVpn()
    def __init__(self):
        pass    

    @classmethod
    def create(cls, *args, **kwargs):
        ret = False
        try:
            upc = cls.upc
            name = kwargs['name']
            iso2 = kwargs.get('iso2', None)
            utils.print_message('| {} | Creating container'.format(name))
            ret = upc.create_container(name=name, iso2=iso2)
            if ret:
                utils.print_message('| {} | Created container'.format(name))
            else:
                utils.print_message('| {} | Cant\'n create container'.format(name))
        except Exception as e:
            utils.print_message("| {} | Error creating container Error: {}".format(name, e))            
        finally:
            cls._send_response(kwargs['task'], ret, kwargs)

    @classmethod
    def destroy(cls, *args, **kwargs):
        ret = False
        try:
            upc = cls.upc
            name = kwargs['name']
            utils.print_message('| {} | Destroying container'.format(name))
            ret = upc.destroy_container(name=name)
            if ret:
                utils.print_message('| {} | Destroyed container'.format(name))
            else:
                utils.print_message('| {} | Cant\'n destroy container'.format(name))
        except Exception as e:
             utils.print_message(
                 "| {} | Error destroying container Error: {}".format(e, name)) 
        finally:
            cls._send_response(kwargs['task'], ret, kwargs)

    @classmethod
    def add_route(cls, *args, **kwargs):
        ret = False
        try:
            route = cls.route
            ip = kwargs['ip']
            every_jump = int(kwargs.get('every_jump', 1))
            utils.print_message('| {0} | Add IP:{0} to Route'.format(ip))
            ret = route.add_routes(ip=ip, every_jump=every_jump)
            if ret:
                utils.print_message('| {0} | Added IP:{0} to Route'.format(ip))
            else:
                utils.print_message('| {0} | Cant\'n add IP:{0} to Route'.format(ip))
        except Exception as e:
            print(" {} | Error adding route Error: {}".format(e, ip))
        finally:
            cls._send_response(kwargs['task'], ret, kwargs)

    @classmethod
    def del_route(cls, *args, **kwargs):
        ret = False
        try:
            route = cls.route
            ip = kwargs['ip']
            every_jump = int(kwargs.get('every_jump', 1))
            utils.print_message('| {0} | Delete IP:{0} to Route'.format(ip))
            ret = route.del_routes(ip=ip, every_jump=every_jump)
            if ret:
                utils.print_message('| {0} | Deleted IP:{0} to Route'.format(ip))
            else:
                utils.print_message('| {0} | Cant\'n delete IP:{0} to Route'.format(ip))
        except Exception as e:
            print(" {} | Error deleting route Error: {}".format(e, ip))
        finally:
            cls._send_response(kwargs['task'], ret, kwargs)

    @classmethod
    def restart_vpn(cls, *args, **kwargs):
        ret = False
        try:
            container_name = kwargs['name']
            iso2 = kwargs.get('iso2', None)
            utils.print_message('| {} | Restart VPN in container'.format(container_name))
            try:
                ret = cls.rvpn.run(container_name=container_name, iso2=iso2)
            except Exception as e:
                print(" {} | Error executing vpn Error: {}".format(e, container_name))
            if ret:
                utils.print_message('| {} | Restarted VPN in container'.format(container_name))
            else:
                utils.print_message('| {} |  Cant\'n restart VPN in container'.format(container_name))
        except Exception as e:
            print(" {} | Error restarting vpn Error: {}".format(e, container_name)) 
        finally:
            cls._send_response(kwargs['task'], ret, kwargs)

    @classmethod
    def restart_vpn_ip(cls, *args, **kwargs):
        ret = False
        try:
            ip = kwargs['ip']
            iso2 = kwargs.get('iso2', None)
            with RedisWrapper() as db:
                container_name = db.get_container_vp_name(ip=ip)
            utils.print_message('| {} | Restarted VPN IP in container'.format(container_name))
            try:
                ret = cls.rvpn.run(container_name=container_name, iso2=iso2)
            except Exception as e:
                print(" {} | Error executing vpn Error: {}".format(e, container_name))
            if ret:
                utils.print_message('| {} | Restarted VPN IP in container'.format(container_name))
            else:
                utils.print_message('| {} | Cant\'n restart VPN IP in container'.format(container_name))
        except Exception as e:
            print(" {} | Error restarting vpn ip Error: {}".format(e, ip)) 
        finally:
            cls._send_response(kwargs['task'], ret, kwargs)
    
    @classmethod
    def _send_response(cls, task, ret, kwargs):
        with RedisWrapper() as db:
            db.send_response(
                settings.settings['redis']['channel_response'],
                task, ret, kwargs
                )