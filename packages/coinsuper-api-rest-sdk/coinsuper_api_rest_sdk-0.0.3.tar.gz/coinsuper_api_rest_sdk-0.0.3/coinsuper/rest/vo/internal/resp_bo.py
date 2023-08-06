#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import coinsuper.rest.coinsuper_util as util
import coinsuper.rest.logger.coinsuper_simple_log as log
import json


def check_res_the_same(source, bo):
    """检查响应结果格式"""
    sorted_source = json.dumps(json.loads(source), sort_keys=True)
    sorted_bo_str = json.dumps(bo, default=lambda obj: obj.__dict__, sort_keys=True)
    log.debug("sorted_source ->\t{}", sorted_source)
    log.debug("sorted_bo_str ->\t{}", sorted_bo_str)
    same = sorted_bo_str == sorted_source
    if not same:
        log.warning("The type -> {} cannot match the result \"data\", please check and upgrade the SDK to new version!",
                    type(bo))
    return same


def print_check_res_the_same(api_name, source, bo):
    log.info(api_name)
    log.info(check_res_the_same(source=source, bo=bo))


# 用户资产信息结果data
class RestUserAssetInfoData:
    """Coinsuepr REST 用户资产信息结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        self.result = RestUserAssetInfoDataResult(**result)


class RestUserAssetInfoDataResult:
    def __init__(self, userNo, email, asset):
        self.userNo = userNo
        self.email = email
        asset_dic = {}
        if util.not_empty(asset):
            for key, val in asset.items():
                asset_dic[key] = RestUserAssetInfoDataResultAsset(**val)
        self.asset = asset_dic


class RestUserAssetInfoDataResultAsset:
    def __init__(self, total, available):
        self.total = total
        self.available = available


# 订单薄行情结果data
class RestOrderBookData:
    """订单薄行情结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        self.result = RestOrderBookDataResult(**result)


class RestOrderBookDataResult:
    def __init__(self, asks, bids):
        l_asks = []
        if util.not_empty(asks):
            for i in asks:
                l_asks.append(RestOrderBookDataResultItem(**i))
        self.asks = l_asks
        l_bids = []
        if util.not_empty(bids):
            for i in bids:
                l_bids.append(RestOrderBookDataResultItem(**i))
        self.bids = l_bids


class RestOrderBookDataResultItem:
    def __init__(self, limitPrice, quantity):
        self.limitPrice = limitPrice
        self.quantity = quantity


# K线行情结果data
class RestKlineData:
    """K线行情结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestKlineDataResult(**i))
        self.result = l_result


class RestKlineDataResult:
    def __init__(self, close, high, low, open, volume, timestamp):
        self.close = close
        self.high = high
        self.low = low
        self.open = open
        self.volume = volume
        self.timestamp = timestamp


# K线行情结果data
class RestTickersData:
    """K线行情结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestTickersDataResult(**i))
        self.result = l_result


class RestTickersDataResult:
    def __init__(self, price, tradeType, volume, timestamp):
        self.price = price
        self.tradeType = tradeType
        self.volume = volume
        self.timestamp = timestamp


# 可交易的交易对列表结果data
class RestSymbolListData:
    """可交易的交易对列表结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestSymbolListResult(**i))
        self.result = l_result


class RestSymbolListResult:
    def __init__(self, symbol, quantityMin, quantityMax, priceMin, priceMax, deviationRatio,
                 quantityScale, amountScale, priceScale):
        self.symbol = symbol
        self.quantityMin = quantityMin
        self.quantityMax = quantityMax
        self.priceMin = priceMin
        self.priceMax = priceMax
        self.deviationRatio = deviationRatio
        self.quantityScale = quantityScale
        self.amountScale = amountScale
        self.priceScale = priceScale


# 下单结果data
class RestPlaceOrderData:
    """下单结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        self.result = RestPlaceOrderDataResult(**result)


class RestPlaceOrderDataResult:
    def __init__(self, orderNo):
        self.orderNo = orderNo


# 撤单结果data
class RestCancelOrderData:
    """撤单结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        self.result = RestCancelOrderDataResult(**result)


class RestCancelOrderDataResult:
    def __init__(self, operate):
        self.operate = operate


# 批量下单结果data
class RestPlaceBatchOrderData:
    """批量下单结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestPlaceBatchOrderResult(**i))
        self.result = l_result


class RestPlaceBatchOrderResult:
    def __init__(self, orderNo, clientOrderId):
        self.orderNo = orderNo
        self.clientOrderId = clientOrderId


# 批量取消委托--根据Coinsuper委托单号列表结果data
class RestBatchCancelByOrderNoListData:
    """批量取消委托--根据Coinsuper委托单号列表结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        self.result = RestBatchCancelByOrderNoListResult(**result)


class RestBatchCancelByOrderNoListResult:
    def __init__(self, successNoList, failResultList):
        self.successNoList = successNoList
        l_failResultList = []
        if util.not_empty(failResultList):
            for i in failResultList:
                l_failResultList.append(RestPlaceCancelFailByOrderNoListResult(**i))
        self.failResultList = l_failResultList


class RestPlaceCancelFailByOrderNoListResult:
    def __init__(self, orderNo, errMsg):
        self.orderNo = orderNo
        self.errMsg = errMsg


# 批量取消委托--根据客户端订单id列表结果data
class RestBatchCancelByClientOrderIdListData:
    """批量取消委托--根据客户端订单id列表结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        self.result = RestBatchCancelByClientOrderIdListResult(**result)


class RestBatchCancelByClientOrderIdListResult:
    def __init__(self, successIdList, failResultList):
        self.successIdList = successIdList
        l_failResultList = []
        if util.not_empty(failResultList):
            for i in failResultList:
                l_failResultList.append(RestPlaceCancelFailByClientOrderIdListResult(**i))
        self.failResultList = l_failResultList


class RestPlaceCancelFailByClientOrderIdListResult:
    def __init__(self, clientOrderId, errMsg):
        self.clientOrderId = clientOrderId
        self.errMsg = errMsg


# 查询委托列表(根据委托单号)结果data
class RestQueryOrderListByOrderNoListData:
    """查询委托列表(根据委托单号)结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestQueryOrderListByOrderNoListResult(**i))
        self.result = l_result


class RestQueryOrderListByOrderNoListResult:
    def __init__(self, orderNo, symbol, action, orderType, priceLimit, quantity, quantityRemaining, amount,
                 amountRemaining, state, fee, utcCreate, utcUpdate):
        self.orderNo = orderNo
        self.symbol = symbol
        self.action = action
        self.orderType = orderType
        self.priceLimit = priceLimit
        self.quantity = quantity
        self.quantityRemaining = quantityRemaining
        self.amount = amount
        self.amountRemaining = amountRemaining
        self.state = state
        self.fee = fee
        self.utcCreate = utcCreate
        self.utcUpdate = utcUpdate


# 查询委托列表(根据客户端单号)结果data
class RestQueryOrderListByClientOrderIdListData:
    """查询委托列表(根据客户端单号)结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestQueryOrderListByClientOrderIdListResult(**i))
        self.result = l_result


class RestQueryOrderListByClientOrderIdListResult:
    def __init__(self, orderNo, clientOrderId, symbol, action, orderType, priceLimit, quantity, quantityRemaining, amount,
                 amountRemaining, state, fee, utcCreate, utcUpdate):
        self.orderNo = orderNo
        self.symbol = symbol
        self.clientOrderId = clientOrderId
        self.action = action
        self.orderType = orderType
        self.priceLimit = priceLimit
        self.quantity = quantity
        self.quantityRemaining = quantityRemaining
        self.amount = amount
        self.amountRemaining = amountRemaining
        self.state = state
        self.fee = fee
        self.utcCreate = utcCreate
        self.utcUpdate = utcUpdate


# 查询订单交易详情结果data
class RestQueryOrderDetailsByOrderNoListData:
    """查询订单交易详情结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestQueryOrderDetailsByOrderNoListResult(**i))
        self.result = l_result


class RestQueryOrderDetailsByOrderNoListResult:
    def __init__(self, orderNo, symbol, action, orderType, priceLimit, quantity, quantityRemaining, amount,
                 amountRemaining, state, detail):
        self.orderNo = orderNo
        self.symbol = symbol
        self.action = action
        self.orderType = orderType
        self.priceLimit = priceLimit
        self.quantity = quantity
        self.quantityRemaining = quantityRemaining
        self.amount = amount
        self.amountRemaining = amountRemaining
        self.state = state
        l_detail = []
        if util.not_empty(detail):
            for i in detail:
                l_detail.append(RestQueryOrderDetailsByOrderNoListDetails(**i))
        self.detail = l_detail


class RestQueryOrderDetailsByOrderNoListDetails:
    def __init__(self, matchType, price, volume, utcDeal, fee, feeCurrency):
        self.matchType = matchType
        self.price = price
        self.volume = volume
        self.utcDeal = utcDeal
        self.fee = fee
        self.feeCurrency = feeCurrency


# 查询历史委托单列表结果data
class RestQueryOrderHistoryData:
    """查询历史委托单列表结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestQueryOrderHistoryResult(**i))
        self.result = l_result


class RestQueryOrderHistoryResult:
    def __init__(self, orderNo, symbol, action, orderType, priceLimit, priceAverage, quantity, quantityRemaining, amount,
                 amountRemaining, state, fee, utcCreate, utcUpdate, detail):
        self.orderNo = orderNo
        self.symbol = symbol
        self.action = action
        self.orderType = orderType
        self.priceLimit = priceLimit
        self.priceAverage = priceAverage
        self.quantity = quantity
        self.quantityRemaining = quantityRemaining
        self.amount = amount
        self.amountRemaining = amountRemaining
        self.state = state
        self.fee = fee
        self.utcCreate = utcCreate
        self.utcUpdate = utcUpdate
        l_detail = []
        if util.not_empty(detail):
            for i in detail:
                l_detail.append(RestQueryOrderHistoryDataDetails(**i))
        self.detail = l_detail


class RestQueryOrderHistoryDataDetails:
    def __init__(self, dealNo, matchType, price, volume, utcDeal, fee, feeCurrency):
        self.dealNo = dealNo
        self.matchType = matchType
        self.price = price
        self.volume = volume
        self.utcDeal = utcDeal
        self.fee = fee
        self.feeCurrency = feeCurrency


# 查询历史成交列表结果data
class RestQueryTradeHistoryData:
    """查询历史成交列表结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(RestQueryTradeHistoryResult(**i))
        self.result = l_result


class RestQueryTradeHistoryResult:
    def __init__(self, dealNo, symbol, matchType, orderNo, orderType, action, price, volume, utcDeal, fee, feeCurrency):
        self.dealNo = dealNo
        self.symbol = symbol
        self.matchType = matchType
        self.orderNo = orderNo
        self.orderType = orderType
        self.action = action
        self.price = price
        self.volume = volume
        self.utcDeal = utcDeal
        self.fee = fee
        self.feeCurrency = feeCurrency


# 查询用户未成交（或未完成）委托单列表结果data
class RestQueryOpenListData:
    """查询用户未成交（或未完成）委托单列表结果data"""
    def __init__(self, timestamp, result):
        self.timestamp = timestamp
        l_result = []
        if util.not_empty(result):
            for i in result:
                l_result.append(i)
        self.result = result

