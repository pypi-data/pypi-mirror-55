#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
from os import path
import sys
from shutil import copyfile

__author__ = "Lennin Caro"
__copyright__ = "Copyright 2019, The Erebo (VPN WAY) Project"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.1.23"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"
__message__ = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
'''


def _copy_files(config_file:str, auth_file:str) -> bool:
    ret = False
    try:
        APP_PATH = path.dirname(path.dirname(path.abspath(__file__)))
        dst_auth_file = f'{APP_PATH}/erebo/config/files_auth.json'
        dst_config_files = f'{APP_PATH}/erebo/config/main.ini'
        x = copyfile(config_file, dst_config_files)
        y = copyfile(auth_file, dst_auth_file)
        if x and y:
            ret = True
    except Exception as e:
        print(e)

    finally:
        return ret


def main_pypi():
    import sys
    print(f"{__message__}")
    print(f"Version PYPI {__version__}")
    config_file, auth_file = sys.argv[1], sys.argv[2]
    if _copy_files(config_file, auth_file):
        from erebo.controllers.daemon_io import Daemon
        dm = Daemon()
        dm.run()
    else:
        print("Error initializing Erebo")


def main(config_file:str, auth_file:str):
    if _copy_files(config_file, auth_file):
        from erebo.controllers.daemon_io import Daemon
        dm = Daemon()
        dm.run()
    else:
        print("Error initializing Erebo")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Erebo')
    parser.add_argument(
        "-c",
        "--config",
        dest='config_file',
        required=True,
        type=str,
        help="location of the configuration file")
    parser.add_argument(
        "-a",
        "--auth",
        dest='auth_file',
        required=True,
        type=str,
        help="location of the auth file")
    args = parser.parse_args()
    print("{}".format(__message__))
    print("Version {}".format(__version__))
    main(args.config_file, args.auth_file)