#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import datetime
import logging

import coinsuper.rest.coinsuper_util as util

is_log_debug = False
is_log_info = True
is_log_warning = True
is_log_error = True
is_print_only = False


def set_node_level(level=logging.INFO):
    logging.basicConfig(level=level)

    global is_log_debug
    global is_log_info
    global is_log_warning
    global is_log_error
    is_log_debug = False
    is_log_info = True
    is_log_warning = True
    is_log_error = True

    if logging.DEBUG == level:
        is_log_debug = True
    elif logging.INFO == level:
        is_log_debug = False
    elif logging.WARNING == level:
        is_log_debug = False
        is_log_info = False
    elif logging.ERROR == level:
        is_log_debug = False
        is_log_info = False
        is_log_warning = False
    else:
        is_log_debug = False
        is_log_info = False
        is_log_error = False
        is_log_warning = False


# 获取当前时间并根据本地时区进行格式化
def now_time_str():
    """获取当前时间并根据本地时区进行格式化"""
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


# print日志
def __log__(msg, level=logging.INFO):
    """print日志"""
    if not is_print_only and logging.DEBUG == level:
        logging.debug(msg)
    elif not is_print_only and logging.INFO == level:
        logging.info(msg)
    elif not is_print_only and logging.WARNING == level:
        logging.warning(msg)
    elif not is_print_only and logging.ERROR == level:
        logging.error(msg)
    else:
        print(msg)


# 打印debug日志
def debug(fmt, *msg):
    """打印debug日志"""
    if is_log_debug:
        if util.is_empty(msg):
            fmt_format = fmt
        else:
            fmt_format = fmt.format(*msg)
        last_msg = "{}\t[DEBUG]:\t{}".format(now_time_str(), fmt_format)
        __log__("\033[36m{}\033[0m".format(last_msg), logging.DEBUG)


# 打印info日志
def info(fmt, *msg):
    """打印info日志"""
    if is_log_info:
        if util.is_empty(msg):
            fmt_format = fmt
        else:
            fmt_format = fmt.format(*msg)
        last_msg = "{}\t[INFO]:\t{}".format(now_time_str(), fmt_format)
        __log__("\033[36m{}\033[0m".format(last_msg), logging.INFO)


# 打印warning日志
def warning(fmt, *msg):
    """打印warning日志"""
    if is_log_error:
        if util.is_empty(msg):
            fmt_format = fmt
        else:
            fmt_format = fmt.format(*msg)
        last_msg = "{}\t[WARNING]:\t{}".format(now_time_str(), fmt_format)
        __log__("\033[33m{}\033[0m".format(last_msg), logging.WARNING)


# 打印error日志
def error(fmt, *msg):
    """打印error日志"""
    if is_log_error:
        if util.is_empty(msg):
            fmt_format = fmt
        else:
            fmt_format = fmt.format(*msg)
        last_msg = "{}\t[ERROR]:\t{}".format(now_time_str(), fmt_format)
        __log__("\033[31m{}\033[0m".format(last_msg), logging.ERROR)

