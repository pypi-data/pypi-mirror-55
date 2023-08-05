#!/usr/bin/python3
# -*- coding: utf-8 -*-

errors = {
    "JSONDecodeError": {
        'code': 300,
        'msg': 'the body of request doesnt have json format'
    },
    "ValidationError": {
        'code': 302,
        'msg': 'error in the params of json object'
    },
    "DataError": {
        'code': 500,
        'msg': 'error in the data'
    },
    "ConectionError": {
        'code': 403,
        'msg': 'error in the conection'
    },
    "UnauthorizedError": {
        'code': 506,
        'msg': 'unauthorized login'
    },
    "UnauthorizedTokenError": {
        'code': 401,
        'msg': 'unauthorized token'
    },
    "ExpiredTokenError": {
        'code': 408,
        'msg': 'token has expired'
    },
    "NotAuthorizationTokenError": {
        'code': 402,
        'msg': 'missing authorization'
    },
    "ExternalError": {
        'code': 405,
        'msg': 'error connecting with external server'
    }
}