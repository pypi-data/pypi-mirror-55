#!/usr/bin/python3
# -*- coding: utf-8 -*-
import hashlib
import requests
import random
import re
import fnmatch
import subprocess
import linecache
import sys
import difflib
import decimal
from json import load, loads, dump
from os import environ, listdir, walk, path
from typing import List, Dict, Tuple, Set
from datetime import datetime
from lockfile import locked
from statistics import mean
from time import sleep
import erebo.settings.settings as settings


def clean_text(text_to_covert: str) -> str:
        """Function 'get_base_regex_expression'.
            Return regular expresion to find in a text

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            text_to_analize (:obj:`str`):  text to analyze.

        Returns:
            :obj:`str` successful, :obj:`None`  otherwise.

        """
        
        text_to_covert = text_to_covert.lower().strip()
        regex_spacechars = (
            ';',
            '-',
            ',',
            '\n',
            ':',
            '_'
        )
        for regex_char in regex_spacechars:
            text_to_covert = text_to_covert.replace(regex_char, ' ')
        
        regex_metachars = (
            '\\\\',
            '.',
            '^',
            ']',
            '[',
            '$',
            '|',
            '?',
            '*',
            '{',
            '}',
            '(',
            ')',
            '/',
            '!',
        )
        for regex_char in regex_metachars:
            text_to_covert = text_to_covert.replace(regex_char, ' ')
        
        special_chars = (
            ('á','a'),
            ('é','e'),
            ('í','i'),
            ('ó','o'),
            ('ú','u'),
            ('à','a'),
            ('è','e'),
            ('ì','i'),
            ('ò','o'),
            ('ù','u'),
            ('ñ','n'),
        )
        for special_char in special_chars:
            text_to_covert = text_to_covert.replace(
                special_char[0], special_char[1])
        text_to_covert = ' '.join([
            wr for wr in text_to_covert.split(' ') 
            if wr != ''])
        return text_to_covert.replace(' +',' ')

def ping_vpn(proxy: str = None):
    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
    ret = {"code": 200, "response": {}}
    try:
        url = 'http://ifconfig.co/json'
        ret['response'] = loads(requests.request(
            'GET',
            url,
            proxies=proxies,
            timeout=15
        ).text)
    except Exception:
        ret['code'] = 400
    return ret

def generate_hash(text):
    aux = hashlib.sha224()
    aux.update(text.encode('utf-8'))
    return aux.hexdigest()

def get_enviroment():
    # enviroments = load(open('erebo/config/enviroment.json'))
    enviroments = load_enviroment()
    sc_enviroment = environ.get('sc_enviroment', 'media')
    file_name = enviroments.get(sc_enviroment, 'media.ini')
    ret = {'file_name': file_name, 'sc_enviroment': sc_enviroment}
    return ret

def copy_file(dirpath: str, file:str, container_name: str, 
        container_dirpath: str) -> bool:
    ret = False
    if dirpath[-1] == '/':
        dirpath = dirpath[:-1]
    if container_dirpath[-1] == '/':
        container_dirpath = container_dirpath[:-1]
    container_path = ':'.join((container_name, container_dirpath))
    filepath = '/'.join((dirpath, file))
    cmd = ['docker', 'cp', filepath, container_path ]
    try:
        subprocess.check_call(cmd)
        ret = True
    except subprocess.CalledProcessError as e:
        print(" {} | Error coping auth  Error: {}".format(e, container_name))
    return ret

def to_route(src_ip: str, to_ip: str, jump: int, add: bool,
        every_jump: int = 1) -> bool:
    # every_jump make x connection continues in the same ip
    # this work to get the external ip in te connection
    ret = False
    action = 'A' if add else 'D'
    jump = int(jump)
    # multiply jump for each every_jump to allow connecting to the same ip fox every_jump times
    jump *= every_jump
    for x in range(every_jump):
        jump -= x
        str_cmd = '''
            iptables 
            -t nat 
            -{} 
            PREROUTING 
            -s {} 
            -i eth0 
            -p tcp 
            --dport 80 
            -m statistic 
            --mode nth 
            --every {} 
            --packet 0 
            -j DNAT 
            --to-destination {}:3128'''.format(action, src_ip, jump, to_ip)
        try:
            subprocess.check_call(str_cmd.split())
            ret = True
        except subprocess.CalledProcessError as e:
            print("Error {}".format(e))
    return ret

def deny_all(add: bool) -> bool:
    ret = False
    action = 'A' if add else 'D'
    str_cmd = '''
        iptables 
        -{} 
        INPUT 
        -p tcp 
        -i eth0 
        --dport 80 
        -j REJECT'''.format(action)
    try:
        subprocess.check_call(str_cmd.split())
        ret = True
    except subprocess.CalledProcessError as e:
        print("Error {}".format(e))
    return ret

def route_target(add: bool) -> bool:
    ret = False
    action = 'A' if add else 'D'
    # str_cmd = '''
    #     iptables 
    #     -t nat 
    #     -{} 
    #     POSTROUTING 
    #     -j MASQUERADE'''.format(action)
    str_cmd = '''
        iptables 
        -t nat 
        -{} 
        POSTROUTING -p tcp
        -j MASQUERADE'''.format(action)
    try:
        subprocess.check_call(str_cmd.split())
        ret = True
    except subprocess.CalledProcessError as e:
        print("Error {}".format(e))
    return ret

def get_location_from_file(vpn_name: str, file_name: str):
    # first group is to Country
    # second group is to location if exist
    country = ''
    info = ''
    files_auth = load_vpns_config()
    regex_compiles = files_auth[vpn_name]['regex_location']
    for regex_compile in regex_compiles:
        cp = re.compile(regex_compile, re.IGNORECASE)
        locations = re.match(cp, file_name)
        try:
            country = clean_text(locations.group(1))
        except Exception:
            pass
        try:
            info = clean_text(locations.group(2))
        except Exception:
            pass

        if country:
            break
    ret = {
        "country": country,
        "info": info
    }
    return ret

def print_message(message: str):
    print('{1}  {0}'.format(
        message,
        datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))

def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    ret = {
        'type': "exception",
        'file_name': filename,
        'line': lineno,
        'expresion': line.strip(),
        'error': exc_obj
    }
    return ret

def alias_acuraccy(text_src: str, text_compare: str) -> List:
        ret = []
        only_title = 0
        text_clean = tuple(clean_text(text_compare).split(' '))
        alias = text_src.split('###')
        acum_acc = []
        for title in alias:
            accuracy = 0
            clean_alias = clean_text(title)                                
            title_split = tuple(clean_alias.split(' '))
            tmp_list = []                    
            for row in text_clean:
                tmp_list.append((
                    row, 
                    difflib.SequenceMatcher(
                        None, title_split[0], row).ratio()))
            first_word = max(tmp_list, key=lambda x: x[1])[0]
            first_word_position = text_clean.index(first_word)
            cant_words = len(title_split)
            compare_words = ' '.join(
                text_clean[first_word_position:first_word_position + cant_words])
            accuracy = difflib.SequenceMatcher(
                None, clean_alias, compare_words).ratio()
            acum_acc.append(accuracy)
        acc_mean = mean(acum_acc)
        if len(acum_acc) == 1:
            only_title = 1
        ret.append({
            "alias": text_src,
            "accuracy": decimal.Decimal(round(acc_mean,3)).quantize(
                decimal.Decimal('0.000'), rounding=decimal.ROUND_UP),
            "only_title": only_title
        })
        return ret

def get_external_ip(container_name, retry: int = 15) -> str:
    cnt = 1
    result = ''
    while True:
        response = ping_vpn()
        if response['code'] == 200 and response['response']:
            result = response['response']['ip']
            break
        sleep(0.3)
        cnt += 1
        if cnt > retry:
            print_message('| {} | \tStep: Error getting VPN external IP  Error: 1005'.format(container_name))
            break
    return result

def get_vpn_external_ip(container: Dict, external_ip: str, retry: int = 35) -> Dict:
    result = ''
    cnt = 1
    while True:
        response = ping_vpn(container["ip_addrs"]+':'+container["port"])
        if (response['code'] == 200 and response['response'] and 
                response['response']['ip'] != external_ip):
            result = response['response']
            break
        sleep(0.3)
        cnt += 1
        if cnt > retry:
            print_message('| {} | \tStep: Error getting VPN external IP  Error: 1005'.format(container['name'])
            )
            break
    return result

def load_vpns_config(file_location: str = None) -> Dict:
    try:
        if not file_location:
            file_location = f'{settings.APP_PATH}/config/files_auth.json'
        ret = load(open(file_location))
    except FileNotFoundError:
        print_message('| {} | \tStep: Error Open file {}'.format('', file_location))
    finally:
        return ret

def load_countries(file_location: str = None) -> Dict:
    try:
        if not file_location:
            file_location = f'{settings.APP_PATH}/config/countries.json'
        ret = load(open(file_location, 'r'))
    except FileNotFoundError:
        print_message('| {} | \tStep: Error Open file {}'.format('', file_location))
    finally:
        return ret

def load_enviroment(file_location: str = None) -> Dict:
    try:
        if not file_location:
            file_location = f'{settings.APP_PATH}/config/enviroment.json'
        ret = load(open(file_location, 'r'))
    except FileNotFoundError:
        print_message('| {} | \tStep: Error Open file {}'.format('', file_location))
    finally:
        return ret