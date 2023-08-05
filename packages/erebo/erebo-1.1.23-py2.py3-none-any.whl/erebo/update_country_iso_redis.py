#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import fnmatch
from json import load, loads, dump
from os import environ, listdir, walk, path
from typing import List, Dict, Tuple, Set
import erebo.settings.settings as settings
import erebo.core.utils as utils
from erebo.model.rediss import RedisWrapper

def _list_files (directory: str) -> Dict:
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
    _, _, filenames = [val for val in walk(directory)][0]
    files = [
        fname
        for fname in filenames
        if re.match(includes, fname)
    ]
    return files

def _find_vpn_country(config: List, files: List, iso2: str) -> List:
    vpn_files = []
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

def get_list_countries_iso2() -> Dict:
    files_auth = utils.load_vpns_config()
    # files_auth = load(open('config/files_auth.json'))
    countries = utils.load_countries()
    providers = [(k, v['directory']) for k, v in files_auth.items()]
    ret = {}
    for provider in providers:
        provider_name = provider[0]
        files = _list_files(provider[1])
        config = files_auth[provider_name]['regex_location']
        provider_iso2 = {}
        for iso2, _ in countries.items():
            cnt_files = len(_find_vpn_country(config, files, iso2))
            if cnt_files > 0:
                provider_iso2[iso2] = cnt_files
        ret[provider_name] = provider_iso2
    return ret
            
def get_list_countries_iso2_total() -> Dict:
    list_countries = get_list_countries_iso2()
    list_iso2 = [] 
    for _, v in list_countries.items(): 
        list_iso2 += list(v.keys()) 
    set_iso2 = set(list_iso2)  
    ret = {} 
    for iso2 in set_iso2: 
        cnt = 0 
        for _,v in list_countries.items(): 
            cnt += v.get(iso2, 0) 
        ret[iso2] = cnt
    return ret

def main():
    lst_countries = get_list_countries_iso2_total()
    with RedisWrapper() as db:
        _ = db.add_country_iso_list(lst_countries)

if __name__ == "__main__":
    print("Updating country list in Redis")
    main()
