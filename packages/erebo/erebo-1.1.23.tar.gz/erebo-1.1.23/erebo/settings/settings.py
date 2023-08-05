#!/usr/bin/python3
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from json import load
from os import path, environ
# import sys
# from platform import node


settings = dict()
APP_PATH = path.dirname(path.dirname(path.abspath(__file__)))
ROOT_PATH = path.dirname(APP_PATH)


def basepath(*path_add):
    return path.join(APP_PATH, *path_add)


# **************************************************************
# DIRECTORY
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sistema de archivos, rutas a directorios de la aplicación
#
# storage: Directorio principal de almacenamiento
# tmp: Directorio temporal
# install: Directorio con contenido de instalación
# dump: Ficheros dump en caso de errores criticos
# uploads: Directorio subida de ficheros
# vault: Directorio de certificados
# template: Directorio base de templates
# schema: Directorio de definición de schemas
# ------------------------------------------------------------//
settings['storage.path'] = basepath('storage')
settings['tmp.path'] = basepath('storage', 'tmp')
settings['install.path'] = basepath('storage', 'install')
settings['dump.path'] = basepath('storage', 'dump')
settings['uploads.path'] = basepath('storage', 'uploads')


# **************************************************************
# CONFIGURATION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Archivos de configuración
#
# main: Fichero de configuración principal
# env.main: Fichero de configuración principal del entorno
# ------------------------------------------------------------//
# enviroments = load(open('erebo/config/enviroment.json'))
enviroments = load(open(f'{APP_PATH}/config/enviroment.json'))
file_name = enviroments.get(environ.get('sc_enviroment', ''), 'main.ini')

settings['config.file.main'] = basepath('config', file_name)
print('Using enviroment: {}'.format(settings['config.file.main']))
# settings['config.file.env'] = basepath('config', 'main.env.ini')
# Gestor de configuración
config = ConfigParser(allow_no_value=True)
config.read((settings['config.file.main'],))
# enviroment
settings['enviroment'] = environ.get('sc_enviroment', 'main')
# Redis
settings['redis'] = {}
settings['redis']['host'] = config.get('Redis', 'host')
settings['redis']['port'] = config.get('Redis', 'port')
settings['redis']['passw'] = config.get('Redis', 'passw')
settings['redis']['dbname'] = config.get('Redis', 'dbname')
settings['redis']['channel'] = config.get('Redis', 'channel')
settings['redis']['channel_response'] = config.get('Redis', 'channel_response')
# file
settings['ovpn_root_dir'] = config.get('Files', 'ovpn_root_dir')
# sudo
settings['sudo_user'] = config.get('Sudo', 'user')
settings['sudo_pass'] = config.get('Sudo', 'passw')