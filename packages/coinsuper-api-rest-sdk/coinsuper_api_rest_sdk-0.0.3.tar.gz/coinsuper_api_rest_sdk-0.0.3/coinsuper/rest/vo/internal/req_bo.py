#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from coinsuper.rest.coinsuper_util import not_empty


class RestRequestKlineRange:
    RANGE_5MIN = "5min"
    RANGE_15MIN = "15min"
    RANGE_30MIN = "30min"
    RANGE_1HOUR = "1hour"
    RANGE_6HOUR = "6hour"
    RANGE_12HOUR = "12hour"
    RANGE_1DAY = "1day"


class RestUserAssetInfoReq:
    """Coinsuper API REST查询用户资产信息 - 请求参数"""
    def __init__(self, currencyList):
        if currencyList is not None:
            self.currencyList = currencyList


class RestOrderBookReq:
    """Coinsuper API REST获取订单薄行情 - 请求参数"""
    def __init__(self, symbol, num):
        self.symbol = symbol
        self.num = num


class RestKlineReq:
    """Coinsuper API REST获取K线行情 - 请求参数"""
    def __init__(self, symbol, num, range):
        self.symbol = symbol
        self.num = num
        self.range = range


class RestTickersReq:
    """Coinsuper API REST获取K线行情 - 请求参数"""
    def __init__(self, symbol):
        self.symbol = symbol


class RestSymbolListReq:
    """Coinsuper API REST获取可交易的交易对列表 - 请求参数"""
    def __init__(self):
        pass


class RestBuyOrderReq:
    """Coinsuper API REST下买单 - 请求参数"""
    def __init__(self, symbol, priceLimit, orderType, quantity, amount, clientOrderId):
        self.symbol = symbol
        self.priceLimit = priceLimit
        self.orderType = orderType
        self.quantity = quantity
        self.amount = amount
        if not_empty(clientOrderId):
            self.clientOrderId = clientOrderId


class RestSellOrderReq:
    """Coinsuper API REST下卖单 - 请求参数"""
    def __init__(self, symbol, priceLimit, orderType, quantity, amount, clientOrderId):
        self.symbol = symbol
        self.priceLimit = priceLimit
        self.orderType = orderType
        self.quantity = quantity
        self.amount = amount
        if not_empty(clientOrderId):
            self.clientOrderId = clientOrderId


class RestCancelOrderReq:
    """Coinsuper API REST取消委托 - 请求参数"""
    def __init__(self, orderNo):
        self.orderNo = orderNo


class RestPlaceBatchOrderReq:
    """Coinsuper API REST下卖单 - 请求参数"""
    def __init__(self, symbol, priceLimit, orderType, action, quantity, amount, clientOrderId):
        self.symbol = symbol
        self.priceLimit = priceLimit
        self.orderType = orderType
        self.action = action
        self.quantity = quantity
        self.amount = amount
        self.clientOrderId = clientOrderId


class RestBatchCancelOrderReq:
    """Coinsuper API REST批量取消委托 - 请求参数"""
    def __init__(self, orderNoList, clientOrderIdList):
        if not_empty(orderNoList):
            self.orderNoList = orderNoList
        if not_empty(clientOrderIdList):
            self.clientOrderIdList = clientOrderIdList


class RestQueryOrderListReq:
    """Coinsuper API REST查询委托列表 - 请求参数"""
    def __init__(self, orderNoList, clientOrderIdList):
        if not_empty(orderNoList):
            self.orderNoList = orderNoList
        if not_empty(clientOrderIdList):
            self.clientOrderIdList = clientOrderIdList


class RestQueryOrderDetailsReq:
    """Coinsuper API REST查询订单交易详情 - 请求参数"""
    def __init__(self, orderNoList):
        self.orderNoList = orderNoList


class RestQueryOrderHistoryReq:
    """Coinsuper API REST查询订单交易详情 - 请求参数"""
    def __init__(self, symbol, utcStart, utcEnd, startOrderNo, withTrade, size):
        self.symbol = symbol
        self.utcStart = utcStart
        self.utcEnd = utcEnd
        if startOrderNo is not None:
            self.startOrderNo = startOrderNo
        if withTrade is not None:
            self.withTrade = withTrade
        if size is not None:
            self.size = size


class RestQueryTradeHistoryReq:
    """Coinsuper API REST查询历史成交列表 - 请求参数"""
    def __init__(self, symbol, utcStart, utcEnd, startDealNo, size):
        self.symbol = symbol
        self.utcStart = utcStart
        self.utcEnd = utcEnd
        if startDealNo is not None:
            self.startDealNo = startDealNo
        if size is not None:
            self.size = size


class RestQueryOpenListReq:
    """Coinsuper API REST查询历史成交列表 - 请求参数"""
    def __init__(self, symbol, num):
        self.symbol = symbol
        self.num = num

