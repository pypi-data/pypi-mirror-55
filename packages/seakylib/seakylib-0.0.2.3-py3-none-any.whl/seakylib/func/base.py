#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/8/14 12:05


import argparse
import json
import os
import pickle as pk
import re
import sys
import time
import traceback
from collections import OrderedDict
from functools import wraps
from pathlib import Path
from pprint import pprint

from ..func.log import make_logger
from ..os.info import get_pwd
from ..os.oper import path_open


def func_done(name=None):
    return 'func {} done.'.format(name if name else sys._getframe().f_back.f_code.co_name)


def count_time(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        count_in_class = False
        if len(args) > 0:
            if hasattr(args[0], '__dict__') and not callable(args[0]):
                self = args[0]
                count_in_class = True
        start_time = time.time()
        result = f(*args, **kwargs)
        elapsed_time = round(time.time() - start_time, 2)
        ip = None
        if count_in_class:
            # 放到self.cache['timer']中
            if hasattr(self, 'cache') and isinstance(self.cache, dict):
                if not self.cache.get('timer'):
                    self.cache['timer'] = OrderedDict()
                self.cache['timer'][f.__name__] = elapsed_time
                if self.cache.get('debug') or (hasattr(self, 'debug') and getattr(self, 'debug')):
                    if hasattr(self, 'info'):
                        ip = self.info.get('snmp', {}).get('peername') or self.info.get('auth', {}).get('ip')
                    elif hasattr(self, 'ip'):
                        ip = self.ip
                    self.log.debug(
                        '{0:.2f}s {1}{2}.'.format(elapsed_time, f.__name__, ' on {}'.format(ip) if ip else ''))
        else:
            if True or kwargs.get('debug'):
                print('{0:.2f}s {1}{2}.'.format(elapsed_time, f.__name__, ' on {}'.format(ip) if ip else ''))
        return result

    return wrap


def is_instance(obj):
    '''对象是一个实例'''
    if hasattr(obj, '__dict__') and not callable(obj):
        return True


def catch_exception(ignore=False, retry=0):
    '''
    :param ignore: 不记录错误
    :param retry: 重试次数
    :return:
    如果 kwargs中含有expose_exception，忽略catch
    '''

    def deco(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'expose_exception' in kwargs:
                expose_exception = kwargs.pop('expose_exception')
                if expose_exception:
                    return f(*args, **kwargs)
            in_class = False
            if len(args) > 0:
                if is_instance(args[0]):
                    self = args[0]
                    in_class = True
            i = 0
            while i <= retry:
                try:
                    excep = False
                    result = f(*args, **kwargs)
                    break
                except AssertionError as e:
                    excep, message, trace = True, '{}'.format(e), '{}'.format(traceback.format_exc())
                except Exception as e:
                    excep, message, trace = True, '{}'.format(e), '{}'.format(traceback.format_exc())
                # print('--{}--'.format(i), retry, self.ip, f, trace)
                i += 1
            if not excep:
                if in_class:
                    self.cache['exception']['critical'] = False
                return result
            else:
                verbose = kwargs.get('verbose')
                if in_class:
                    if 'errors' not in self.cache['exception']:
                        self.cache['exception']['error'] = []
                    self.cache['exception']['critical'] = not ignore
                    self.cache['exception']['error'].append(
                        {'func': f.__name__, 'error_message': '{}'.format(message),
                         'error_traceback': '{}'.format(trace)})
                    if hasattr(self, 'verbose') and getattr(self, 'verbose'):
                        verbose = verbose or self.verbose
                    if self.log and not ignore:
                        self.log.debug(trace)
                return False, trace if verbose else message

        return wrap

    return deco


def run_func(obj, **kwargs):
    '''
    运行传入的函数，func/(func, (...))/(func, {...}), kwargs也会被传递给func
    :param obj:
    :return:
    '''
    if hasattr(obj, '__call__'):
        return obj()
    elif isinstance(obj, tuple):
        if len(obj) == 2:
            func, args = obj
            if isinstance(args, tuple):
                return func(*args, **kwargs)
            elif isinstance(args, dict):
                return func(**args, **kwargs)
        else:
            func, *args = obj
            return func(*args, **kwargs)
    return False, '{} can not be called'.format(obj)


@catch_exception()
def run_functions(*funcs, message=None, order='and', watchdog=None, **kwargs):
    '''
    funcs见run_func
    如果是and，所有func返回True，最后返回True
    如果是or，任意func返回True即返回True，否则返回False
    watchdog: 额外判断函数
    '''

    for func in funcs:
        is_ok, _message = run_func(func)
        assert is_ok, _message
        x, y = run_func(watchdog)
        if not x:
            is_ok, _message = x, '{} ({})'.format(_message, y)
        if order == 'and':
            if not is_ok:
                return is_ok, _message
        elif order == 'or':
            if is_ok:
                return is_ok, _message
    # 如果是and，跳出循环表明都执行成功；如果是or，跳出循环表明都执行失败
    if order == 'and':
        return True, message if message else 'run_fucs successfully.'
    elif order == 'or':
        return False, message if message else 'run_fucs fail.'


class MyClass:
    def __init__(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
            path_output
            path_temp
            log:    customer log
            log_params
            show_tick  显示count_time的值
            log_params  make_logger的参数
            quite
            debug   logging.debug
        '''
        self.kwargs = kwargs
        self.pwd = get_pwd()
        self.path_output = self.pwd / Path(kwargs.get('path_output', 'output'))
        self.path_temp = self.pwd / Path(kwargs.get('path_temp', 'temp'))
        # 默认log是打印到console
        log_params = kwargs.get('log_params', {})
        if kwargs.get('debug'):
            log_params.update({'level': 'DEBUG'})
        # self.log = kwargs.get('log', make_logger(self.__class__.__name__, **log_params))
        # 两个类建立默认log时，前者会没有输出？
        self.log = kwargs['log'] if 'log' in kwargs else make_logger(self.__class__.__name__, **log_params)
        self.quite = kwargs.get('quite')
        # cache存放过程数据, 最好不要放入无法dump的数据
        self.cache = {'error': [], 'timer': OrderedDict(), 'exception': {'critical': False}, 'message': ''}
        self.verbose = kwargs.get('verbose')

    def show_verbose(self, *obj):
        if self.verbose:
            for o in obj:
                pprint(o) if isinstance(o, (list, dict)) else print(o)

    def log_error(self, s, *kwargs):
        '''在这里记录错误'''
        self.cache['error'].append(s)
        self.log.error(s, *kwargs)


def load_data(filename, store_dir='temp', work_dir=None, mode='json'):
    work_dir = work_dir or get_pwd()
    dpath = Path(work_dir) / store_dir
    fpath = dpath / os.fsdecode(filename)
    if os.path.exists(str(fpath)):
        try:
            if mode == 'pickle':
                return True, pk.load(path_open(str(fpath), 'rb'))
            elif mode == 'json':
                return True, json.load(path_open(str(fpath), 'r'))
        except Exception as e:
            return False, ''


def dump_data(obj, filename, store_dir='temp', work_dir=None, mode='json'):
    work_dir = work_dir or get_pwd()
    dpath = Path(work_dir) / store_dir
    fpath = dpath / os.fsdecode(str(filename))
    dpath.mkdir(exist_ok=True)
    if mode == 'pickle':
        pk.dump(obj, path_open(str(fpath), 'wb'))
    elif mode == 'json':
        json.dump(obj, path_open(str(fpath), 'w'), indent='  ')
    return True, ''


# def a(func):
#     if func
#
# # save load需要编写
# def sl(obj, filename, func=None, save=True, load=True, store_dir='temp', work_dir=None, mode='json'):
#     work_dir = work_dir or get_pwd()
#     dpath = Path(work_dir) / store_dir
#     fpath = dpath / os.fsdecode(filename)
#     if load and fpath.exists():
#         data = json.load(path_open(fpath))
#         return True, data
#     self.kwargs['os'] = self.data_in_db['device']['os']
#     is_ok, result = self.inspect(method='snmp' if self.os == 'comware' else 'cli')
#     assert is_ok, result
#     self.cache['inspect_done'] = True
#     if self.kwargs.get('save') and is_ok:
#         json.dump(self.info, path_open(path_data, 'w'))
#     self.data_new = self.info
#     return is_ok, result


def func_result(save=False, load=False, ident_key=None, mark=None, func_dump=None, func_load=None):
    '''
    保存成 <store_dir>/[mark_]<func_name>[_ident_key]，一些特殊的对象无法保存
    :param save:
    :param load:
    :param ident_key:
    :param path:
    :param mark:
    :param func_dump:
    :param func_load:
    :return:
    '''

    def deco(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            filename = f.__name__
            if ident_key and ident_key in kwargs:
                filename += '_{}={}'.format(ident_key, kwargs[ident_key])
            if mark:
                filename = '{}_{}'.format(mark, filename)
            else:
                if 'mark' in kwargs:
                    filename = '{}_{}'.format(kwargs['mark'], filename)
            filename += '.result'
            filename = filename.replace('/', '-')
            in_class = False
            if len(args) > 0:
                if is_instance(args[0]):
                    self = args[0]
                    in_class = True
                    if hasattr(self, 'path_temp'):
                        filename = Path(self.path_temp) / filename
            if load and filename.is_file():
                r, d = load_data(filename)
                if r:
                    return func_load(d['result']) if func_load else d['result']
                else:
                    return
            result = f(*args, **kwargs)
            if save:
                r, d = dump_data({'result': func_dump(result) if func_dump else result,
                                  'func': f.__name__, 'args': str(args), 'kwargs': str(kwargs)}, filename)
            return result

        return wrap

    return deco


class ArgParseClass:
    def __init__(self, description='', group=None):
        '''
        :param description:
        :param group: add_all()中优先于__init__
        '''
        self.parser = argparse.ArgumentParser(description=description)
        self.group = group
        self.groups = {}
        if group:
            self.groups[group] = self.parser.add_argument_group(title=group)
        self.opts = []
        # require 强制，hidden 隐藏arg, forbidden 禁止某些arg。
        # 这些列表是为继承时检查，都不需要加--
        self.require = []
        self.hidden = []
        self.forbidden = []

    def add_all(self):
        # 上层可以按需重写 add_all
        pass

    def add_base(self, group='Base'):
        self.add('--verbose', action='store_true', help='verbose mode', group=group)

    def add_notify(self, group='Notify'):
        self.add('--yx', action='store_true', help='yixin', group=group)
        self.add('--popo', action='store_true', help='popo', group=group)
        self.add('--sms', action='store_true', help='sms', group=group)

    def add(self, *args, **kwargs):
        opt = args[0]
        # 隐藏参数
        if re.sub('^-+', '', opt) in self.hidden:
            return
        if opt in self.opts:
            return
        title = kwargs.get('group') or self.group
        if title:
            if title not in self.groups:
                self.groups[title] = self.parser.add_argument_group(title=title)
            parser = self.groups[title]
        else:
            parser = self.parser
        if 'group' in kwargs:
            del kwargs['group']
        self.opts.append(opt)
        parser.add_argument(*args, **kwargs)

    def parse(self):
        self.args = self.parser.parse_args()
        return self.args

    def dict(self):
        return self.parse().__dict__

    def check_args(self):
        '''
        检查require和forbidden列表
        :return:
        '''
        cmd = ' '.join(sys.argv)
        if '--help' in cmd:
            return
        for x in self.require:
            if not re.search(' -+{}'.format(x), cmd):
                self.parser.print_help()
                print('\narg "--{}" is required !!!\n'.format(x))
                exit(1)
        for x in sys.argv[1:]:
            if x.startswith('--') and re.sub('^-+', '', x) in self.forbidden:
                self.parser.print_help()
                print('\narg "{}" is forbidden !!!\n'.format(x))
                exit(1)
