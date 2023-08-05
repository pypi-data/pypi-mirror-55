#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/10/30 10:57

import hashlib
import os
import re
import shutil
import socket
from pathlib import Path


def path_open(pathname, mode='r', **kwargs):
    '''
    defaultencoding和LC_ALL/LC_CTYPE/LANG变量有关，在pycharm中运行时，需要配置任一变量为C.UTF-8，
    如果zh_CN.UTF-8，有可能会改变term的语言
    '''
    sep = os.fsdecode(str(pathname)).split('/')[:-1]
    if re.search(r'(w|a)', mode):
        for i, name in enumerate(sep):
            if not name:
                continue
            _path = Path('/'.join(sep[:i + 1]))
            if not _path.is_dir():
                _path.mkdir()
    return open(os.fsencode(str(pathname)), mode, **kwargs)


def path_delete(pathname, force=False):
    '''
    删除空目录/文件
    :param pathname:
    :param force:   如果目录非空，也删除
    :return:
    '''
    pathname = Path(pathname)
    if pathname.exists():
        if pathname.is_file():
            pathname.unlink()
            return True, 'remove file {}.'.format(pathname)
        elif pathname.is_dir():
            if not [x for x in pathname.glob('*')]:
                pathname.rmdir()  # 空目录
                return True, 'remove empty dir {}.'.format(pathname)
            elif force:
                shutil.rmtree(str(pathname))
                return True, 'remove dir {} with files.'.format(pathname)
        return True, '{} is not file or dir.'.format(pathname)
    return True, '{} is not exist.'.format(pathname)


def path_copy(src, dst, overwrite=False, violent=False, **kwargs):
    '''
    :param src:
    :param dst:
    :param overwrite:   覆盖文件
    :param violent:     暴力，如果存在dst目录，删除后复制
    :param kwargs:
    :return:
    '''
    src, dst = Path(src), Path(dst)
    msg = '{} copy as {}.'.format(src, dst)
    if src.is_dir():
        if not dst.exists():
            shutil.copytree(src, dst)
            return True, msg
        else:
            if dst.is_dir():
                if violent:
                    shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    return True, msg
                else:
                    for x in src.glob('*'):
                        is_ok, _msg = path_copy(x, dst / x.name)
                        if not is_ok:
                            return is_ok, _msg
            else:
                return False, '{} is dir, but {} is a exist file.'.format(src, dst)
    else:
        if not dst.exists():
            shutil.copy2(src, dst)
            return True, msg
        else:
            if overwrite:
                shutil.copy2(src, dst)
                return True, '{} overwrite {}.'.format(src, dst)
            else:
                md5src = hashlib.md5(path_open(src)).hexdigest()
                md5dst = hashlib.md5(path_open(dst)).hexdigest()
                if md5src == md5dst:
                    return True, '{} is same as {}.'.format(dst, src)
                else:
                    return False, '{} is exist and different from {}.'.format(dst, src)


def check_port(ip, port):
    '''
    check port is available
    :param ip:
    :param port:
    :return:
    '''
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)
    try:
        sk.connect((ip, port))
        is_ok, msg = True, 'port {} is open.'.format(port)
    except Exception as e:
        is_ok, msg = False, 'port {} is close.'.format(port)
    sk.close()
    return is_ok, msg
