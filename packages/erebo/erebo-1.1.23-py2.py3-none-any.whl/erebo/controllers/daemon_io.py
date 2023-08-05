#!/usr/bin/python3
# -*- coding: utf-8 -*-
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from json import loads
# import erebo.controllers.test_len as tl
import erebo.core.utils as utils
import erebo.settings.settings as settings
from erebo.model.rediss import RedisWrapper
from erebo.controllers.controller import Controller
from erebo.controllers.daemon import DaemonFnc

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"


class Daemon(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self):
        self.futures = []

    def _fnc_callback(self, msg:str):
        msg_dict = loads(msg)
        ct =  Controller()
        if msg_dict.get('task', None):
            ct.main(msg_dict)

    def get_message(self, callback, **kwargs):
        db = RedisWrapper()
        pubsub = db.get_pubsub(channel=settings.settings['redis']['channel'])
        while True:
            msg = pubsub.get_message()
            if msg:
                if msg.get('type', '') == 'message':
                    callback(msg=msg['data'].decode('utf8'), **kwargs)

    def proc_channel(self):
        while True:
            try:
                print("connecting to channel")
                self.get_message(callback=self._fnc_callback)
            except ConnectionError:
                print("PPL {}".format(utils.print_exception()))
                print("closed channel")
            except Exception as e:
                print("PPL {}".format(utils.print_exception()))
                print("Error Exited from PPL - Error:{}").format(e)
            
    # def get_message(self, callback, **kwargs):
    #     try:
    #         db = RedisWrapper()
    #         pubsub = db.get_pubsub(channel='test')
    #         while True:
    #             msg = pubsub.get_message()
    #             if msg:
    #                 if msg.get('type', '') == 'message':
    #                     callback(msg=msg['data'].decode('utf8'), **kwargs)
    #     except Exception:
    #         print("PPL {}".format(utils.print_exception()))
    #         print("Error Exited from PPL - Error:{}").format(e)

    # def proc_channel(self):
    #     self.get_message(callback=self._fnc_callback)

    
    def proc_test(self):
        pass
        # tl.run()

    def proc_daemon_fnc(self):
        dm = DaemonFnc()
        # dm.restart_vpn_time(time_seg=300)
        dm.restart_vpn_time(time_seg=0)

    def run(self):
        executor = ThreadPoolExecutor(max_workers=2)
        executor.submit(self.proc_channel)
        # executor.submit(self.proc_test)
        # executor.submit(self.proc_daemon_fnc)