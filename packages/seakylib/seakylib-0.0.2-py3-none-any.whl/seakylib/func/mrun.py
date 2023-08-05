#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/4/20 14:44

import queue
import time
import traceback
from multiprocessing import Process, Manager
from random import randint

from ..func.base import ArgParseClass
from ..func.base import MyClass
from ..net.db import MyModel


class MultiRun(MyClass):
    def __init__(self, func, func_kws, process_num=5, inline=False, func_common_kw=None, func_common_kw_obj=None,
                 **kwargs):
        '''
        :param func: 处理函数
        :param func_kws:    需要处理的参数
        :param process_num: 进程数
        :param inline: 单进程运行
        :param func_common_kw: 函数通用参数, 不能放入log object
        :param func_common_kw_obj: 函数通用参数, 可放入object，如log，因为object不能被dump，所以单独处理
        :return
        '''
        MyClass.__init__(self, **kwargs)
        self.func = func
        self.func_kws = func_kws
        self.process_num = process_num
        self.func_common_kw = {} if func_common_kw is None else func_common_kw
        self.func_common_kw_obj = {} if func_common_kw_obj is None else func_common_kw_obj
        self.inline = inline
        m = Manager()
        self.q_input = m.Queue()
        self.q_output = m.Queue()

    def job(self, process_i):
        while True:
            try:
                v = self.q_input.get_nowait()
                is_ok, result = self.func(**v['kw'], **self.func_common_kw_obj)
                v.update({'is_ok': is_ok, 'result': result})
                self.q_output.put(v)
            except queue.Empty:
                break
            except Exception as e:
                self.log.info(traceback.format_exc())
                break

    def run(self):
        if not isinstance(self.func_kws, list):
            return False, 'func_kws is not list.'
        idxes = []
        for i, kw in enumerate(self.func_kws, 1):
            idx = id(kw)
            kw.update(self.func_common_kw)
            d = {'order_in': i, 'idx': idx, 'kw': kw}
            idxes.append(idx)
            self.q_input.put(d)

        if self.inline:
            self.job(1)
        else:
            process_num = min(self.process_num, len(self.func_kws))
            ps = []
            for process_i in range(1, process_num + 1):
                process = Process(target=self.job, args=([process_i]))
                ps.append(process)
                process.start()
            for i, p in enumerate(ps):
                p.join()

        outputs = {}
        for i in range(1, self.q_output.qsize() + 1):
            d = self.q_output.get_nowait()
            d['order_out'] = i
            outputs[d['idx']] = d
        return True, [outputs.get(idx, {'is_ok': False, 'message': 'result is not exist.'}) for i, idx in
                      enumerate(idxes)]


def update_results(model, datas, key, sql=None, cls_conn_str=None, session=None, last_cols=None, timed=False):
    '''
    :param model: 结果表格
    :param datas: 运行结果
    :param key: 主键
    :param sql: 如果无sql，则返回表格数据
    :param cls_conn_str: db连接字串
    :param session:     db session
    :param last_cols:   [col1, col2], 更新时需要保留的上一次状态。model中需要有 col1_last, col2_last字段
    :param timed:   记录时间
    :return:
    '''
    if model.__class__ == MyModel:
        mm = model
    else:
        if cls_conn_str:
            MyModel.cls_conn_str = cls_conn_str
            mm = MyModel(model)
        elif session:
            mm = MyModel(model, session=session)
        else:
            return
    if not last_cols:
        last_cols = [col.replace('_last', '') for col in mm.cols_name if col.endswith('_last')]
    if sql:
        is_ok, data_old = mm.query(sql=sql, key=key)
    else:
        is_ok, data_old = mm.query(key=key)
    for i, v in enumerate(datas):
        k = key(v) if hasattr(key, '__call__') else v[key]
        if k in data_old:
            _keys = list(v.keys())
            for col in _keys:
                if col not in mm.cols_name:
                    continue
                if col in last_cols:
                    v['{}_last'.format(col)] = data_old[k][col]
        count_fail_col = 'failed'
        if 'is_ok' in v and count_fail_col in mm.cols_name:
            if k in data_old:
                _count = data_old[k][count_fail_col]
                if not _count:
                    _count = 0
            else:
                _count = 0
            if not v['is_ok']:
                v[count_fail_col] = _count + 1
            else:
                v[count_fail_col] = _count
        if 'is_ok' in v:
            v['is_ok'] = 1 if v['is_ok'] else 0

    is_ok, result = mm.update(data_new=datas, data_old=data_old, key=key, timed=timed)
    return is_ok, result


class MrunArgParse(ArgParseClass):
    def __init__(self, *args, **kwargs):
        ArgParseClass.__init__(self, *args, **kwargs)
        ArgParseClass.add_base(self)
        if not kwargs.get('delay'):
            self.add_multi()

    def add_multi(self, group='Multi Process'):
        self.add('--process_num', type=int, default=100, help='multi process number', group=group)
        self.add('--inline', action='store_true', default=False, help='inline mode', group=group)


if __name__ == '__main__':
    def test(i):
        # must return is_ok, message
        t = randint(0, 3)
        time.sleep(t)
        msg = 'i am {}, waiting {}.'.format(i, t)
        print(msg)
        return True, msg


    mr = MultiRun(func=test, func_kws=[{'i': x} for x in range(5)], process_num=3, inline=False)
    print(mr.run())
