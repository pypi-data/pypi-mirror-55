#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import hashlib
import json

import requests
import time
import coinsuper.rest.error.coinsuper_rest_error as cs_error
import coinsuper.rest.logger.coinsuper_simple_log as log


class CoinsuperAuth:
    """
    Coinsuper API认证相关参数
    """

    def __init__(self, accesskey, secretkey):
        # 密钥对，请自行申请并妥善保管（注：正式环境是不同的）
        self.accesskey = accesskey
        self.secretkey = secretkey


class CoinsuperServerConfig:
    """
    Coinsuper 服务端相关配置
    """

    def __init__(self, scheme, host, port):
        if scheme is not None:
            self.__scheme = scheme
        if host is not None:
            self.__host = host
        if host is not None:
            self.__port = port

    def prefix(self):
        return self.__scheme + "://" + self.__host + ":" + self.__port

    @classmethod
    def create_default(cls):
        """
        默认生产服务端配置
        """
        scheme = "https"
        host = "api.coinsuper.info"
        port = "443"
        return cls(scheme, host, port)


# 将class转dict,以_开头的属性不要
def props_param(obj):
    """将class转dict,以_开头的属性不要"""
    if isinstance(obj, list):
        pr = []
        for i in obj:
            pr.append(props_param(i))
        return pr
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value) and not name.startswith('_'):
            pr[name] = value
    return pr


# 验证签名
def get_request_data(params, coinsuper_auth):
    if not isinstance(params, dict):
        params = props_param(params)
    # 组装验签参数
    if isinstance(params, list):
        # 如果value是list，则整个作为字符串，并将转换后的json串去掉多余的空格
        param_for_sign = {"data": json.dumps(params, separators=(',', ':'))}
    else:
        param_for_sign = params.copy()
    timestamp = int(time.time())
    param_for_sign["accesskey"] = coinsuper_auth.accesskey
    param_for_sign["secretkey"] = coinsuper_auth.secretkey
    param_for_sign["timestamp"] = timestamp
    sign = '&'.join(['{}={}'.format(k, param_for_sign[k]) for k in sorted(param_for_sign.keys())])
    # 生成签名
    md5_str = hashlib.md5(sign.encode("utf8")).hexdigest()
    # 组装请求参数
    request_data = {
        "common": {
            "accesskey": coinsuper_auth.accesskey,
            "timestamp": timestamp,
            "sign": md5_str
        },
        "data": params
    }
    return request_data


def http_post(server_config, api_uri, params):
    log.debug("API uri->{} request params:->\t{}", api_uri, params)
    r = requests.post(server_config.prefix() + api_uri, json=params, timeout=1)
    result = r.json()
    log.debug(result)
    if result is None:
        raise cs_error.CoinsuperRestLocalError(**cs_error.unknown_local_error)
    if result["code"] != "1000":
        raise cs_error.CoinsuperRestApiError(result["code"], result["msg"])
    return result["data"]
