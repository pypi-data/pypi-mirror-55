#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/8/20 10:15

from ..func.base import MyClass, ArgParseClass, func_done
from ..probe.miko.connect import BaseDevice
from ..func.mrun import MrunArgParse
from ..probe.snmp import Snmp


class NetDeviceClass(MyClass):
    def __init__(self, ip=None, _init_conn=True, *args, **kwargs):
        '''
        :param ip:
        :param miko_param:
        :param snmp_param:
        :param _init_conn: os可能需要通过查询得到，设置_init_conn以延迟
        :param args:
        :param kwargs:
        '''
        MyClass.__init__(self, *args, **kwargs)
        self.ip = ip
        if 'log' not in kwargs:
            kwargs['log'] = self.log
        self._init_conn = _init_conn
        if self._init_conn:
            self.init_conn()

    def init_conn(self):
        self.miko_param = self.kwargs.get('miko_param')
        self.snmp_param = self.kwargs.get('snmp_param')
        if isinstance(self.miko_param, dict):
            if self.ip:
                self.miko_param.update({'ip': self.ip})
            self.kwargs.update(self.miko_param)
            self.cli = BaseDevice(**self.kwargs)
            if not self.ip:
                self.ip = self.cli.ip
        if isinstance(self.snmp_param, dict):
            if self.ip:
                self.snmp_param.update({'ip': self.ip})
            self.kwargs.update(self.snmp_param)
            self.snmp = Snmp(**self.kwargs)
            if not self.ip:
                self.ip = self.snmp.ip
        return True, func_done()

    def do(self):
        '''
('comware', '10.163.105.55'),
('vrp', '10.163.49.81'),
('ios', '10.163.108.122'),
('nxos', '10.163.172.32'),
('dnos', '10.163.81.25'),
('ftos', '10.60.3.25'),
('ibmnos', '10.163.73.35'),
('powerconnect', '10.163.73.144'),
('iosxe', '10.80.172.13'),
('iosxr', '10.163.105.10'),
        :return:
        '''
        funcs = {'comware': self.do_comware,
                 'vrp': self.do_vrp,
                 'ios': self.do_ios,
                 'iosxe': self.do_iosxe,
                 'iosxr': self.do_iosxr,
                 'nxos': self.do_nxos,
                 'dnos': self.do_dnos,
                 'ftos': self.do_ftos,
                 'powerconnect': self.do_powerconnect,
                 'ibmnos': self.do_ibmnos,
                 'junos': self.do_junos,
                 }
        return funcs[self.cli.os]()

    def do_comware(self):
        return False, 'no code.'

    def do_vrp(self):
        return False, 'no code.'

    def do_ios(self):
        return False, 'no code.'

    def do_iosxe(self):
        return False, 'no code.'

    def do_iosxr(self):
        return False, 'no code.'

    def do_nxos(self):
        return False, 'no code.'

    def do_dnos(self):
        return False, 'no code.'

    def do_ftos(self):
        return False, 'no code.'

    def do_ibmnos(self):
        return False, 'no code.'

    def do_powerconnect(self):
        return False, 'no code.'

    def do_junos(self):
        # {'os': 'junos', 'ip': '95.3-1.124.252'}
        return False, 'no code.'


class NeteaseDeviceClass(NetDeviceClass):
    def __init__(self, *args, **kwargs):
        NetDeviceClass.__init__(self, *args, **kwargs)


class NetDeviceArgParse(ArgParseClass):
    def __init__(self, *args, **kwargs):
        ArgParseClass.__init__(self, *args, **kwargs)
        if not kwargs.get('delay'):
            self.add_device()

    def add_device(self, group='Single Device'):
        self.add('--ip', required=True, help='target IP address', group=group)
        self.add('--os', default='', help='OS of device', group=group)


class MultiNetDeviceArgParse(MrunArgParse):
    def __init__(self, *args, **kwargs):
        MrunArgParse.__init__(self, *args, **kwargs)
        if not kwargs.get('delay'):
            self.add_multi_device()

    def add_multi_device(self, group='Multi Device'):
        self.add('--limit', type=int, default=100000, help='query limit', group=group)
        self.add('--ips', default='', help='spec ips', group=group)
        self.add('--os', default='', help='os of single jobs, do NOT check libre', group=group)
