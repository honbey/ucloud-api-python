#!/usr/bin/env python

'''
Filename: main.py
Author:   honbey
Date:     2022-04-30
Description:

'''

import os
import sys
import time
import hashlib
import requests

API_URL = 'https://api.ucloud.cn'
REGION = 'cn-bj2'
PROJECT_ID = os.getenv('UCLOUD_PROJECT_ID')
PUBLIC_KEY = os.getenv('UCLOUD_PUBLIC_KEY')
PRIVATE_KEY = os.getenv('UCLOUD_PRIVATE_KEY')


def to_str(k: str, v: any) -> str:
    '''K-V data must be concatenated and sorted by ascent alphabet.

    :param str k:
        key
    :param v:
        value
    :return:
        concatenated string contains K and V
    :rtype:
        str
    '''
    if isinstance(v, list):
        s = ''
        for i in v:
            s += to_str('', i)

        return k + s

    elif isinstance(v, dict):
        v = dict(sorted(v.items(), key=lambda x: x[0], reverse=False))

        s = ''
        for kk, vv in v.items():
            s += to_str(kk, vv)

        return k + s

    else:
        return k + _str(v)


def _str(v):
    '''Converting value to correct string.

    Boolean must be `true` or `false`, float must convert to 
    integer which can completely divide 1.

    :param v:
        value
    :return:
        converted string
    :rtype:
        str
    '''
    if isinstance(v, bool):
        return 'true' if v else 'false'

    if isinstance(v, float):
        return str(int(v)) if v % 1 == 0 else str(v)

    return str(v)


def calc_sign(d: dict, k: str) -> str:
    '''Calculating signature of final concatenated string.

    :param dict d:
        data required by API except signature
    :param str k:
        private key
    :return:
        signature of request
    :rtype:
        str
    '''
    return hashlib.sha1((to_str('', d) + k).encode('utf-8')).hexdigest()


c = {
    'Region': REGION,
    'ProjectId': PROJECT_ID,
    'PublicKey': PUBLIC_KEY,
}

d = {
    'Action': 'GetCertificateV2',
    'Offset': 0,
    'Limit': 10,
}

d.update(c)

d['Signature'] = calc_sign(d, PRIVATE_KEY)

python_version = '{v[0]}.{v[1]}.{v[2]}'.format(v=sys.version_info)
sdk_version = '0.0.0'

h = {
    'User-Agent': 'Mozilla/5.0 (CLI; Python/{python_version}) Python-SDK/{sdk_version}'.format(
        python_version=python_version, sdk_version=sdk_version
    ),
    'Content-Type': 'application/json',
    'U-Timestamp-Ms': str(int(round(time.time() * 1000))),
}


if __name__ == '__main__':
    resp = requests.post(
        url=API_URL,
        json=d,
        headers=h,
    )
    print(resp.json())

