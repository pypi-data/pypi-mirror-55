#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import re
import fnmatch
from json import load, loads, dump
from os import environ, listdir, walk, path
from typing import List, Dict, Tuple, Set
from datetime import datetime
from erebo.model.rediss import RedisWrapper
import erebo.settings.settings as settings
import erebo.core.utils as utils


def get_auth_available(vpn_name: Tuple):
    files_auth = utils.load_vpns_config()
    # files_auth = load(open('config/files_auth.json'))
    ret = {
        "file": vpn_name[1],
        "vpn_name": vpn_name[0],
        "directory": files_auth[vpn_name[0]]['directory'],
        "container_dirpath": files_auth[vpn_name[0]]['container_dirpath']
    }
    if ret['directory'][-1] == '/':
        directory = ret['directory'][:-1]
    else:
        directory = ret['directory']
    ret['full_path'] = '/'.join((directory, vpn_name[1]))
    return ret

def list_files (directory: str) -> Dict:
    """Return ovpn data with a list of files in key filenames
    
    Arguments:
        directory {str} -- dir path
    
    Returns:
        Dict -- ovpn file data with a list of ovpn files
    """
    if directory[-1] == '/':
        directory = directory[:-1]
    includes = ['*.ovpn']
    includes = r'|'.join([fnmatch.translate(x) for x in includes])
    dirpath, dirnames, filenames = [val for val in walk(directory)][0]
    files = [
        fname
        for fname in filenames
        if re.match(includes, fname)
    ]
    ret = {
        "dirpath": dirpath,
        "dirnames": dirnames,
        "filenames": files
    }
    return ret

def get_ovpn_filename(directory: str) -> Dict:
    """Get a random file from list_files function
    
    Arguments:
        directory {str} -- dir path
    
    Returns:
        Dict -- ovpn file data
    """
    ret = {}
    filenames = list_files(directory)
    max_files = len(filenames['filenames'])
    if max_files > 0:
        rnd_number = random.randint(0, max_files - 1)
        filename = filenames['filenames'][rnd_number]
        ret = {
            "dirpath": filenames['dirpath'],
            "filename": filename,
            "full_path": "/".join((filenames['dirpath'], filename))
        }
    return ret

def get_ovpn_filename_iso(vpn_avaliable: Dict, iso2: str = None) -> Dict:
    """Get a random file from list_files function
    
    Arguments:
        directory {str} -- dir path
    
    Returns:
        Dict -- ovpn file data
    """
    ret = {}
    vpns = utils.load_vpns_config()
    # vpns = load(open('config/files_auth.json'))
    vpn_name = vpn_avaliable['vpn_name']
    vpn_location = vpns[vpn_name]['regex_location']
    vpn_files = list_files(vpns[vpn_name]['directory'])
    vpns_country = find_vpn_country(vpn_location, vpn_files['filenames'], iso2)
    max_files = len(vpns_country)
    if max_files > 0:
        rnd_number = random.randint(0, max_files - 1)
        filename = vpns_country[rnd_number]
        ret = {
            "dirpath": vpn_files['dirpath'],
            "filename": filename,
            "full_path": "/".join((vpn_files['dirpath'], filename))
        }
    return ret

def replace_auth_user(ovpn_file: str, auth_user_pass_file: str) -> bool:
    """Replaces the "auth-user-pass" line in the .ovpn file  adding the path of the
       file where the user and password are stored
    Arguments:
        ovpn_file {str} -- dir path to ovpn file
        auth_user_pass_file {str} -- dir path to file with user and pass
    
    Returns:
        bool -- True if could be replace
    """
    ret = False
    line_id = None
    try:
        with open(ovpn_file , 'r') as op: 
            lines = op.readlines()
        for idx, item in enumerate(lines): 
            if "auth-user-pass" in item: 
                line_id = idx    
                break
        if line_id:
            lines[line_id] = " ".join(("auth-user-pass", auth_user_pass_file)) + "\n"
            with open(ovpn_file , 'w') as op: 
                op.writelines(lines)
            ret = True
    except Exception as e:
        print(" {} | Error replacing auth user Error: {}".format(e, auth_user_pass_file))
    finally:
        return ret

def get_vpn_name(iso2: str = None) -> Tuple:
    vpns = utils.load_vpns_config()
    # vpns = load(open('config/files_auth.json')) 
    rows = [] 
    all_vpn = {}
    
    for vpn in vpns.keys(): 
        auths = [{  
            (vpn, k): v['max_connections']} 
            for k, v in vpns[vpn]['files_auth'].items()
            if v['max_connections'] > 0] 
        rows += auths
    for row in rows: 
        all_vpn = {**all_vpn, **row}
    with RedisWrapper() as db:
        used_vpn = db.get_used_vpn()
    avaliable_vpn = [key for key in all_vpn if all_vpn[key] - used_vpn.get(key,0) > 0]
    if iso2:
        vpn_iso = get_vpn_location(avaliable_vpn, iso2)
        avaliable_vpn = [x for x in avaliable_vpn if x[0] in vpn_iso] 
    return _get_random_vpn_name(avaliable_vpn)

def _get_random_vpn_name(vpns: List) -> Tuple:
    max_files = len(vpns)
    rnd_number = random.randint(0, max_files - 1)
    return vpns[rnd_number]

def decrease_auth(vpn_name: str, auth: str) -> bool:
    ret = True
    return ret

def get_vpn_location(avaliable_vpn: List, iso2: str):
    ret = {}
    vpns = utils.load_vpns_config()
    # vpns = load(open('config/files_auth.json'))
    aval_vpn = set(x[0] for x in avaliable_vpn)
    for vpn_name in aval_vpn:
        vpn_files = list_files(vpns[vpn_name]['directory'])
        vpn_location = vpns[vpn_name]['regex_location']
        ret[vpn_name] = find_vpn_country(vpn_location, vpn_files['filenames'], iso2)
    ret = [key for key in ret if len(ret[key]) > 0]
    return ret

def find_vpn_country(config: List, files: List, iso2: str):
    vpn_files = []
    # countries = load(open('config/countries.json', 'r'))
    countries = utils.load_countries()
    country = countries[iso2]
    country_name = country['country'].strip().lower()
    country_iso3 = country['iso3'].strip().lower()
    country_iso2 = iso2.strip().lower()
    cp = re.compile(config[0], re.IGNORECASE)
    for i in files:
        try:
            ret = re.search(cp, i).group(1) 
            ret = ret.replace('-', '').replace('_', ' ').strip().lower()
            if ret == country_iso2:
                vpn_files.append(i)
            elif ret == country_iso3:
                vpn_files.append(i)
            elif ret in country_name:
                vpn_files.append(i)
        except Exception as e:
            print(e)
    return vpn_files