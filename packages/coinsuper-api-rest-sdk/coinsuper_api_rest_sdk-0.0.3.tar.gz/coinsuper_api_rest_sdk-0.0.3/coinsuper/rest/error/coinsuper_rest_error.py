#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-


class LocalErrorCons:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


class CoinsuperRestError(RuntimeError):
    def __init__(self, code, msg):
        super().__init__(self, "code:\"{}\", msg:\"{}\"".format(code, msg))
        self.code = code
        self.msg = msg


class CoinsuperRestLocalError(RuntimeError):
    """本地异常"""
    def __init__(self, code, msg):
        super().__init__(self, code, msg)


class CoinsuperRestApiError(RuntimeError):
    """服务端异常提示"""
    def __init__(self, code, msg):
        super().__init__(self, code, msg)

# 未知的本地异常
unknown_local_error = CoinsuperRestLocalError("L001", "unknown local exception, please check the request param or the pure response result")
# 到API服务端的网络可能有异常
api_network_maybe_wrong = CoinsuperRestLocalError("L002", "network to API server maybe wrong")
# 无效的API accessKey或secretKey
api_keys_invalid = CoinsuperRestLocalError("L003", "API key(s) are invalid")
# 无效的data 请求参数
api_request_data_params_invalid = CoinsuperRestLocalError("L004", "API request param(s) in data are invalid, please see the API doc for detail")
