#!/usr/bin/python3
# -*- coding: utf-8 -*-
import docker
import time
import hashlib
import os
import signal
from typing import List, Dict, Tuple, Set 
from docker.types import LogConfig
from time import sleep
import erebo.core.utils as utils
import erebo.core.vpn_utils as vutils
import erebo.settings.settings as settings
from erebo.model.rediss import RedisWrapper



class DockerProject(object):

    def __init__(self):
        # self.client = docker.from_env()
        # self.client = docker.DockerClient(version='1.24')
        self.client = docker.DockerClient()
        self.containers = list(dict())
        self.logs_check = {}

    def container_run(
            self, image: str, name: str, command: str, volumes: list = [],
            devices: list = [], cap_add: list = [], dns: list = [],
            detach: bool = True, tty: bool = True, stdout: bool = True,
            stderr: bool = True, log_config = {}, environment = [], ports: Dict = {}):
        """[summary]
        
        Arguments:
            image {str} -- [description]
            name {str} -- [description]
            command {str} -- [description]
        
        Keyword Arguments:
            volumes {list} -- [description] (default: {[]})
            devices {list} -- [description] (default: {[]})
            cap_add {list} -- [description] (default: {[]})
            dns {list} -- [description] (default: {[]})
            detach {bool} -- [description] (default: {True})
            tty {bool} -- [description] (default: {True})
            stdout {bool} -- [description] (default: {True})
            stderr {bool} -- [description] (default: {True})
            log_config {dict} -- [description] (default: {{}})
            environment {list} -- [description] (default: {[]})
            port {dict} -- [description] (default: {{}})
        
        Returns:
            [type] -- [description]
        """


        #log_config format:
        # {"max_size": "1g", "labels": "erebo"}
        volumes_dicts = dict()
        if log_config:
            lc = LogConfig(
                type=LogConfig.types.JSON,
                config=log_config
            )
        else:
            lc = LogConfig(
                type=LogConfig.types.JSON,
                config={"max-size": "1g", "labels": "erebo"}
            )
        for volume in volumes:
            vol_host, vol_container, vol_permission = volume.split(':')
            volumes_dicts[vol_host] = {
                'bind': vol_container,
                'mode': vol_permission
            }
        container = None
        restart_policy = {
            "Name": "unless-stopped",
            "MaximumRetrycount": 0,
        }
        container = self.client.containers.run(
            image=image, name=name, detach=detach, tty=tty, stdout=stdout,
            stderr=stderr, volumes=volumes_dicts, devices=devices,
            cap_add=cap_add, dns=dns, command=command,
            restart_policy=restart_policy, environment=environment,
            log_config=lc, ports=ports)
        container_dict = {
            "name": name,
            "container": container,
            "status": "run",
            "created_at": time.time()
        }
        self.containers.append(container_dict)
        return container

    def container_exec(
            self, name: str, command: str, stdout: bool = True,
            stderr: bool = True, stdin: bool = False, tty: bool = False,
            detach: bool = True):
        """[summary]
        
        Arguments:
            name {str} -- [Container name]
            command {str} -- [CMD to execute]
        
        Keyword Arguments:
            stdout {bool} -- [Attach to stdout] (default: {True})
            stderr {bool} -- [Attach to stderr] (default: {True})
            stdin {bool} -- [Attach to stdin] (default: {False})
            tty {bool} -- [Allocate a pseudo-TTY.] (default: {False})
            detach {bool} -- [If true, detach from the exec command] (default: {True})
        """
        con = self.get_container(name=name)
        run_cmd = con.exec_run(cmd=command, detach=detach)
        return run_cmd

    def container_logs(self, name) -> bool:
        container = self.get_container(name)
        if container:
            return container.logs()
        return False

    def container_wait(self, name) -> bool:
        container = self.get_container(name)
        if container:
            container.wait()
            return True
        return False

    def container_stop(self, name) -> bool:
        container = self.get_container(name)
        if container:
            try:
                container.stop()
                return True
            except Exception:
                return False
        return False

    def container_start(self, name):
        container = self.get_container(name)
        if container:
            try:
                container.start()
                return True
            except Exception:
                return False
        return False

    def container_remove(self, name):
        container = self.get_container(name)
        if container:
            try:
                container.remove()
                return True
            except Exception:
                return False
        return False

    def container_stop_remove(self, name):
        container = self.get_container(name)
        if container:
            if (self.container_stop(name) and
               self.container_remove(name)):
                return True
        return False

    def get_container(self, name):
        try:
            return [
                x
                for x in self.get_containers()
                if x.name == name][0]
        except Exception as e:
            utils.print_message('| {} | ERROR getting container Err:{}'.format(name, e))

    def get_containers(self, all: bool = True):
        try:
            return self.client.containers.list(all)
        except Exception:
            return None

    def remove_container_name(self, name):
        try:
            for x in self.get_containers():
                if x.name == name:
                    x.remove(force=True)
                    return True
            return False
        except Exception as e:
            utils.print_message('| {} | ERROR removing container next name Err:{}'.format(name, e))
            return None

    def get_container_nextname(self, prefix_name:str) -> str:
        """[summary]
        
        Arguments:
            prefix_name {str} -- [description]
        
        Returns:
            str -- [description]
        """
        try:
            nextdocker = 1
            if self.get_containers() is None:
                print("Create new:" + prefix_name + '_' + str(nextdocker))
                return prefix_name + '_' + str(nextdocker)
            for x in self.get_containers():
                if prefix_name in x.name:
                    if x.status == 'exited':
                        print("Remove and reuse:" + x.name)
                        x.remove()
                        return x.name
                    else:
                        data = x.name.split('_')
                        if 'openvpn' == data[0]:
                            if int(data[2]) >= nextdocker:
                                nextdocker = int(data[2]) + 1
                        # elif 'youtube' == data[0]:
                        #     if int(data[2]) >= nextdocker:
                        #         nextdocker = int(data[2]) + 1
                        else:
                            if int(data[1]) >= nextdocker:
                                nextdocker = int(data[1]) + 1
            print("Create new:" + prefix_name + '_' + str(nextdocker))
            return prefix_name + '_' + str(nextdocker)
        except Exception as e:
            utils.print_message('| {} | ERROR getting container next name Err:{}'.format(prefix_name, e))
            return None

    def get_container_process(self, name: str) -> List:
        container = self.get_container(name=name)
        process = [x for x in container.top()['Processes']]
        return process

    def get_container_process_per_name(self, name:str, proc_name:str) -> List:
        process = self.get_container_process(name)
        proc_list = [x for x in process if proc_name in x[7]]
        return proc_list

    def get_container_info(self, container_name: str) -> Dict:
        result = {}
        try:
            container = self.get_container(name=container_name)
            result = {
                "container": container,
                "name": container.name, 
                "status": container.status, 
                "ip_addrs": container.attrs['NetworkSettings']['IPAddress'],
                "ports": container.attrs['NetworkSettings']['Ports'],
                "port": list(
                    container.attrs['NetworkSettings']['Ports'])[0].split('/')[0]
            }
        except Exception as e:
            utils.print_message('| {} | ERROR getting container info Err:{}'.format(container_name, e))
        finally:
            return result

    def kill_process(self, pids: List, container_name: str) -> bool:
        ret = False
        try:
            for pid in pids:
                utils.print_message('| {} | \tStep: kill PID {}'.format(
                    container_name, pid))
                os.kill(int(pid), signal.SIGKILL)
            ret = True
        except Exception as e:
            utils.print_message(
                '| {} | ERROR killing process Err:{}'.format(pids, e))
        return ret

    def kill_process_sudo(self, pids: List, container_name: str) -> bool:
        ret = False
        command = 'kill -9'
        sudoPassword = settings.settings['sudo_pass']
        try:
            for pid in pids:
                utils.print_message('| {} | \tStep: kill PID {}'.format(
                    container_name, pid))
                os.system(
                    f'echo {str(sudoPassword)}|sudo -S {str(command)} {int(pid)}'
                    )
            ret = True
        except Exception as e:
            utils.print_message(
                '| {} | ERROR killing process Err:{}'.format(pids, e))
        return ret
        

    def exec_vpn(self, container_name:str, iso2: str = None) -> Dict:
        ret = {}
        vpn_name = vutils.get_vpn_name()
        iso2_error = "There are no vpn files from '{}'".format(iso2)
        try:
            auth_file = vutils.get_auth_available(vpn_name)
            if auth_file['full_path']:
                if iso2:
                    ovpn_file = vutils.get_ovpn_filename_iso(auth_file, iso2)
                else:
                    ovpn_file = vutils.get_ovpn_filename(auth_file['directory'])
                replace_auth = vutils.replace_auth_user(
                    ovpn_file['full_path'], auth_file['full_path'])
                if replace_auth:
                    utils.print_message('| {} |\tStep: Saving VPN Info'.format(container_name))
                    with RedisWrapper() as db:
                        db.add_container_auth(container_name=container_name,
                            auth_file=auth_file['file'],
                            vpn_name=auth_file['vpn_name'],
                            vpn_file=ovpn_file['full_path'])
                    if auth_file['container_dirpath'][-1] == '/':
                        auth_file['container_dirpath'] = auth_file['container_dirpath'][:-1]
                    cp_ovpn = utils.copy_file(
                        ovpn_file['dirpath'],
                        ovpn_file['filename'],
                        container_name,
                        auth_file['container_dirpath']
                    )
                    cp_auth = utils.copy_file(
                        auth_file['directory'],
                        auth_file['file'],
                        container_name,
                        auth_file['container_dirpath']
                    )
                    if cp_ovpn and cp_auth:
                        file_name = '/'.join((
                            auth_file['container_dirpath'],
                            ovpn_file['filename'].replace(' ', '\ ')))
                        cmd = "openvpn --config"
                        cmd_exec = ' '.join((cmd, file_name))
                        _ = self.container_exec(container_name, cmd_exec, True)
                        ret = {
                            "container_name": container_name,
                            "auth_file": auth_file['file'],
                            "vpn_name": auth_file['vpn_name'],
                            "vpn_file": ovpn_file['full_path']
                        }
                    else:
                        utils.print_message('| {} | ERROR coping auth and ovpn file Err:{}'.format(container_name, '1001'))
                else:
                    utils.print_message('| {} | ERROR Error in auth file Err:{}'.format(container_name, '1001'))
            else:
                if auth_file:
                    vutils.decrease_auth(vpn_name, auth_file['file'])
                    with RedisWrapper() as db:
                        db.del_container_auth(container_name=container_name)
                utils.print_message('| {} | ERROR There are no free ovpn, all the authentication files have been used Err:{}'.format(container_name, '1001'))
        except Exception as e:
            utils.print_message('| {} | ERROR executing vpn process Err:{}'.format(container_name, e))
            if iso2:
                utils.print_message('| {} | ERROR {}'.format(container_name, iso2_error))
        finally:
            return ret