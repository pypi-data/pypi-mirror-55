#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-


def is_empty(s):
    """判断字符串或集合或dict是否为空"""
    return s is None or len(s) < 1


def not_empty(s):
    """判断字符串或集合或dict是否不为空"""
    return not is_empty(s)
