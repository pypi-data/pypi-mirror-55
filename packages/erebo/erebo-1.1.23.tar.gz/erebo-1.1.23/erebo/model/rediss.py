#!/usr/bin/python3
# -*- coding: utf-8 -*-
import redis
from json import loads, dumps
from typing import List, Dict, Tuple, Set
from hashlib import sha256
from datetime import datetime
from time import sleep
from json import dumps
from collections import Counter
import erebo.settings.settings as settings
import erebo.core.utils as utils
from erebo.core.utils import get_enviroment

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"

class RedisWrapper(object):
    shared_state = {}

    def __init__(self):
        _pool_config = {
            "host": settings.settings['redis']['host'],
            "port": settings.settings['redis']['port'],
            "db": settings.settings['redis']['dbname']
        }
        _pass = settings.settings['redis'].get('passw', None)
        if _pass:
            sha_pass = sha256(_pass.encode('utf8')).hexdigest()
            _pool_config['password'] = sha_pass
        self.__conn_pool = redis.ConnectionPool(**_pool_config)
        self.__conn = redis.Redis(connection_pool=self.__conn_pool)
        self.__sc_enviroment = get_enviroment()['sc_enviroment']
        self.__pubsub = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._RedisWrapper__pubsub:
            self._RedisWrapper__pubsub.unsubscribe()
        if self.__conn_pool:
            self.__conn_pool.disconnect()

    def __del__(self):
        if self._RedisWrapper__pubsub:
            self._RedisWrapper__pubsub.unsubscribe()
        pass

    def ping(self):
        return self.__conn.ping()

    def get_user(self, user: str) -> Dict:
        name = 'users_ws'
        ret = {}
        try:
            con = self.__conn
            rows = con.hget(name=name, key=user)
            ret = loads(rows.decode('utf8'))
        except Exception as e:
            print(e)
        finally:
            return ret

    def add_container(self, container: str, name: str, ip: str,
            local_port: str, remote_port: str, host_ip: str) -> bool:
        name = 'containers'
        ret = False
        data = {
            "id": container.id,
            "ip": ip,
            "host_ip": host_ip,
            "local_port": local_port,
            "remote_port": remote_port
        }
        try:
            con = self.__conn
            _ = con.hset(
                name=name,
                value=dumps(data),
                key=str(container.name)
            )
            ret = True
        except Exception as e:
            utils.print_message('| {} | ERROR adding container in Redis Err:{}'.format(name, e))
        finally:
            return ret

    def get_containers(self) -> Dict:
        name = 'containers'
        ret = []
        try:
            con = self.__conn
            rows = con.hgetall(name=name)
            for row in rows.items():
                row_details = loads(row[1].decode('utf8'))
                ret.append({
                    "name": row[0].decode('utf8'),
                    "id": row_details['id'],
                    "ip": row_details['ip']
                })
        except Exception as e:
            utils.print_message('| {} | ERROR agetting container from Redis Err:{}'.format(name, e))
        finally:
            return ret

    def add_container_auth(self, container_name: str, auth_file: str,
            vpn_name: str, vpn_file: str):
        name = 'containers_auth'
        ret = {}
        vpn_country = utils.get_location_from_file(vpn_name, vpn_file)
        value = {
            "auth_file": auth_file,
            "vpn_name": vpn_name,
            "vpn_file": vpn_file,
            "vpn_country": vpn_country.get('country', '')
        }
        try:
            con = self.__conn
            _ = con.hset(
                name=name,
                value=dumps(value),
                key=container_name
            )
        except Exception as e:
            utils.print_message('| {} | ERROR adding auth data to Redis Err:{}'.format(container_name, e))
        finally:
            return ret

    def get_container_auth(self, container_name: str):
        name = 'containers_auth'
        ret = {}
        try:
            con = self.__conn
            ret = con.hget(name=name, key=container_name)
            ret = loads(ret)
        except Exception as e:
            utils.print_message('| {} | ERROR getting auth data from Redis Err:{}'.format(container_name, e))
        finally:
            return ret

    def del_container_auth(self, container_name: str) -> bool:
        name = 'containers_auth'
        ret = False
        try:
            con = self.__conn
            _ = con.hdel(name, container_name)
            ret = True
        except Exception as e:
            utils.print_message('| {} | ERROR deleting auth data in Redis Err:{}'.format(container_name, e))
        finally:
            return ret

    def del_container(self, container_name: str):
        name = 'containers'
        ret = {}
        try:
            con = self.__conn
            _ = con.hdel(
                name,
                str(container_name),
            )
        except Exception as e:
            utils.print_message('| {} | ERROR deleting container from Redis Err:{}'.format(container_name, e))
        finally:
            return ret

    def add_to_route(self, ip: str, container_ip: str, position: int) -> bool:
        name = 'routes:{}'.format(ip)
        ret = False
        try:
            con = self.__conn
            _ = con.hset(name, key=container_ip, value=position)
        except Exception as e:
            print(e)
        finally:
            return ret

    def get_to_route(self, ip: str):
        name = 'routes:{}'.format(ip)
        ret = []
        try:
            con = self.__conn
            ret = [
                {
                    'ip': k.decode('utf-8'),
                    'position': v.decode('utf-8')}
                for k, v in  con.hgetall(name=name).items()]
        except Exception as e:
            print(e)
        finally:
            return ret

    def del_to_route(self, ip: str, container_ip: str) -> bool:
        name = 'routes:{}'.format(ip)
        ret = False
        try:
            con = self.__conn
            _ = con.hdel(name, container_ip)
        except Exception as e:
            print(e)
        finally:
            return ret

    def add_container_vp_ip(self, container_name: str, value: Dict) -> bool:
        name = 'containers_vpn_ip'
        ret = False
        try:
            con = self.__conn
            _ = con.hset(
                name=name,
                value=dumps(value),
                key=container_name
            )
            ret = True
        except Exception as e:
            utils.print_message('| {} | ERROR adding container ip in Redis Err:{}'.format(container_name, e))
        finally:
            return ret

    def get_container_vp_ip(self, container_name: str) -> bool:
        name = 'containers_vpn_ip'
        ret = False
        try:
            con = self.__conn
            _ = con.hget(name=name, key=container_name)
            ret = True
        except Exception as e:
            utils.print_message('| {} | ERROR getting container ip from Redis Err:{}'.format(container_name, e))
        finally:
            return loads(ret)

    def get_container_vp_name(self, ip: str) -> str:
        name = 'containers_vpn_ip'
        ret = False
        try:
            con = self.__conn
            ret = [
                k.decode('utf-8')
                for k, v in con.hgetall(name=name).items() 
                if loads(v.decode('utf-8'))['ip'] == ip][0]
        except Exception as e:
            utils.print_message('| {} | ERROR getting container name from Redis Err:{}'.format(ip, e))
        finally:
            return ret

    def del_container_vp_ip(self, container_name: str) -> bool:
        name = 'containers_vpn_ip'
        ret = False
        try:
            con = self.__conn
            _ = con.hdel(name, container_name)
            ret = True
        except Exception as e:
            utils.print_message('| {} | ERROR delteing container ip from Redis Err:{}'.format(container_name, e))
        finally:
            return ret

    def get_task(self, channel:str, callback, **kwargs):
        print("wait for message")
        pubsub = self.__conn.pubsub()
        pubsub.subscribe(channel)
        self.__pubsub = pubsub
        while True:
            msg = self.__pubsub.get_message()
            if msg:
                if msg.get('type', '') == 'message':
                    callback(msg=msg['data'].decode('utf8'), **kwargs)

    def get_pubsub(self, channel:str):
        pubsub = self.__conn.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def get_pub(self, channel: str, msg):
        ret = False
        try:
            self.__conn.publish(channel, msg)
            ret = True
        except Exception as e:
            print(e)
        return ret

    def send_response(self, channel: str, task:str, status: bool, msg: str):
        dct_msg =  {
            "task": task,
            "status": status,
            "msg": msg
        }
        msg = dumps(dct_msg)
        self.get_pub(channel=channel, msg = msg)

    def get_used_vpn(self):
        name = 'containers_auth'
        ret = False
        try:
            con = self.__conn
            rows = [
                loads(v.decode('utf-8')) 
                for k, v in con.hgetall(name).items()
            ]
            vpns_used = [
                (x["vpn_name"], x["auth_file"]) 
                for x in  rows
            ]
            ret = dict(Counter(vpns_used)) 
        except Exception as e:
            utils.print_message('| {} | ERROR deleting auth data in Redis Err:{}'.format('', e))
        finally:
            return ret

    def add_country_iso_list(self, country_iso_list: Dict) -> bool:
        name = 'country_iso2_list'
        ret = False
        try:
            con = self.__conn
            _ = self.__conn.delete(name)
            for k, v in country_iso_list.items():
                _ = con.hset(
                    name=name,
                    value=int(v),
                    key=str(k)
                )
            ret = True
        except Exception as e:
            utils.print_message('| ERROR fecth data to Redis Err:{}'.format(e))
        finally:
            return ret