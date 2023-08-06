#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import coinsuper.rest.cns_api as cns_api
import coinsuper.rest.vo.internal.req_bo as req
import coinsuper.rest.vo.internal.resp_bo as resp
import coinsuper.rest.error.coinsuper_rest_error as cs_error
import json

from coinsuper.rest.coinsuper_constant import RestRequestOrderType, RestRequestOrderAction
from coinsuper.rest.coinsuper_util import not_empty, is_empty


# API REST接口列表
class ApiRestEndpoints:
    """API REST接口列表"""

    def __init__(self):
        self.query_asset_info = "/api/v1/asset/userAssetInfo"
        self.get_market_order_book = "/api/v1/market/orderBook"
        self.get_market_kline = "/api/v1/market/kline"
        self.get_market_tickers = "/api/v1/market/tickers"
        self.get_symbol_list = "/api/v1/market/symbolList"
        self.order_buy = "/api/v1/order/buy"
        self.order_sell = "/api/v1/order/sell"
        self.order_cancel = "/api/v1/order/cancel"
        self.order_batch_place = "/api/v1/order/batchPlace"
        self.order_batch_cancel = "/api/v1/order/batchCancel"
        self.query_order_list = "/api/v1/order/list"
        self.query_order_cl_list = "/api/v1/order/clList"
        self.query_order_details = "/api/v1/order/details"
        self.query_order_history = "/api/v1/order/history"
        self.query_order_trade_history = "/api/v1/order/tradeHistory"
        self.query_order_open_list = "/api/v1/order/openList"


# Coinsuper REST接口模型
class CoinsuperRest:
    """Coinsuper REST接口模型"""

    def __init__(self, accesskey, secretkey):
        self.coinsuper_auth = cns_api.CoinsuperAuth(accesskey, secretkey)
        self.server_config = cns_api.CoinsuperServerConfig.create_default()
        self.uri = ApiRestEndpoints()

    # 获取用户账户信息
    def query_asset_info(self, currency_list):
        """获取用户账户信息"""
        if not_empty(currency_list):
            currency_list = ",".join(currency_list)
        params = req.RestUserAssetInfoReq(currency_list)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.query_asset_info,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestUserAssetInfoData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 获取订单薄行情
    def get_market_order_book(self, symbol, num):
        """获取订单薄行情"""
        if is_empty(symbol):
            raise cs_error.api_request_data_params_invalid
        params = req.RestOrderBookReq(symbol=symbol, num=num)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.get_market_order_book,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestOrderBookData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 获取K线行情
    def get_market_kline(self, symbol, num, range):
        """获取K线行情"""
        if is_empty(symbol) or is_empty(range):
            raise cs_error.api_request_data_params_invalid
        params = req.RestKlineReq(symbol=symbol, num=num, range=range)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.get_market_kline,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestKlineData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 获取最新成交行情
    def get_market_tickers(self, symbol):
        """获取最新成交行情"""
        if is_empty(symbol):
            raise cs_error.api_request_data_params_invalid
        params = req.RestTickersReq(symbol)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.get_market_tickers,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestTickersData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 获取可交易的交易对列表
    def get_symbol_list(self):
        """获取可交易的交易对列表"""
        params = req.RestSymbolListReq()
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.get_symbol_list,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestSymbolListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 下限价买单
    def place_buy_limit_order(self, symbol, price_limit, quantity, client_order_id):
        """下限价买单"""
        if is_empty(symbol) or is_empty(price_limit) or is_empty(quantity):
            raise cs_error.api_request_data_params_invalid
        params = req.RestBuyOrderReq(symbol, price_limit, RestRequestOrderType.LMT, quantity, "0", client_order_id)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_buy,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestPlaceOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 下市价买单
    def place_buy_market_order(self, symbol, amount, client_order_id):
        """下市价买单"""
        if is_empty(symbol) or is_empty(amount):
            raise cs_error.api_request_data_params_invalid
        # 若orderType=MKT,则priceLimit, quantity传入"0", amount为用户输入值
        params = req.RestBuyOrderReq(symbol, "0", RestRequestOrderType.MKT, "0", amount, client_order_id)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_buy,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestPlaceOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 下限价卖单
    def place_sell_limit_order(self, symbol, price_limit, quantity, client_order_id):
        """下限价卖单"""
        if is_empty(symbol) or is_empty(price_limit) or is_empty(quantity):
            raise cs_error.api_request_data_params_invalid
        params = req.RestSellOrderReq(symbol, price_limit, RestRequestOrderType.LMT, quantity, "0", client_order_id)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_sell,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestPlaceOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 下市价卖单
    def place_sell_market_order(self, symbol, quantity, client_order_id):
        """下市价卖单"""
        if is_empty(symbol) or is_empty(quantity):
            raise cs_error.api_request_data_params_invalid
        params = req.RestSellOrderReq(symbol, "0", RestRequestOrderType.MKT, quantity, "0", client_order_id)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_sell,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestPlaceOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 取消委托
    def cancel_order(self, order_no):
        """取消委托"""
        if is_empty(order_no):
            raise cs_error.api_request_data_params_invalid
        params = req.RestCancelOrderReq(order_no)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_cancel,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestCancelOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 下批量买单
    def place_batch_buy_order(self, symbol, buy_orders):
        """下批量买单"""
        if is_empty(symbol) or is_empty(buy_orders):
            raise cs_error.api_request_data_params_invalid
        params = []
        for i in buy_orders:
            o = req.RestPlaceBatchOrderReq(symbol, i.priceLimit, i.orderType, RestRequestOrderAction.BUY, i.quantity,
                                           i.amount, i.clientOrderId)
            params.append(o)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_batch_place,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestPlaceBatchOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 下批量卖单
    def place_batch_sell_order(self, symbol, sell_orders):
        """下批量卖单"""
        if is_empty(symbol) or is_empty(sell_orders):
            raise cs_error.api_request_data_params_invalid
        params = []
        for i in sell_orders:
            o = req.RestPlaceBatchOrderReq(symbol, i.priceLimit, i.orderType, RestRequestOrderAction.SELL,
                                           i.quantity, i.amount, i.clientOrderId)
            params.append(o)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_batch_place,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestPlaceBatchOrderData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 批量取消委托--根据Coinsuper委托单号列表
    def batch_cancel_order_by_order_no_list(self, order_no_list):
        """批量取消委托--根据Coinsuper委托单号列表"""
        if is_empty(order_no_list):
            raise cs_error.api_request_data_params_invalid
        order_no_list_str = ",".join(order_no_list)
        params = req.RestBatchCancelOrderReq(orderNoList=order_no_list_str, clientOrderIdList=None)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_batch_cancel,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestBatchCancelByOrderNoListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 批量取消委托--根据客户端订单id列表
    def batch_cancel_order_by_client_order_id_list(self, client_order_id_list):
        """批量取消委托--根据客户端订单id列表"""
        if is_empty(client_order_id_list):
            raise cs_error.api_request_data_params_invalid
        client_order_id_list_str = ",".join(client_order_id_list)
        params = req.RestBatchCancelOrderReq(orderNoList=None, clientOrderIdList=client_order_id_list_str)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.order_batch_cancel,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestBatchCancelByClientOrderIdListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 查询委托列表--根据Coinsuper委托单号列表
    def query_order_list_by_order_no_list(self, order_no_list):
        """查询委托列表--根据Coinsuper委托单号列表"""
        if is_empty(order_no_list):
            raise cs_error.api_request_data_params_invalid
        order_no_list_str = ",".join(order_no_list)
        params = req.RestQueryOrderListReq(orderNoList=order_no_list_str, clientOrderIdList=None)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.query_order_list,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestQueryOrderListByOrderNoListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 查询委托列表--根据客户端订单id列表
    def query_order_list_by_client_order_id_list(self, client_order_id_list):
        """查询委托列表--根据客户端订单id列表"""
        if is_empty(client_order_id_list):
            raise cs_error.api_request_data_params_invalid
        client_order_id_list_str = ",".join(client_order_id_list)
        params = req.RestQueryOrderListReq(orderNoList=None, clientOrderIdList=client_order_id_list_str)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.query_order_cl_list,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestQueryOrderListByClientOrderIdListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 查询订单交易详情--根据Coinsuper委托单号列表
    def query_order_details_by_order_no_list(self, order_no_list):
        """查询订单交易详情--根据Coinsuper委托单号列表"""
        if is_empty(order_no_list):
            raise cs_error.api_request_data_params_invalid
        order_no_list_str = ",".join(order_no_list)
        params = req.RestQueryOrderDetailsReq(order_no_list_str)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.query_order_details,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestQueryOrderDetailsByOrderNoListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 查询历史委托单列表
    def query_order_history(self, symbol, utc_start, utc_end, start_order_no, with_trade, size):
        """查询历史委托单列表"""
        if is_empty(symbol) or utc_start is None or utc_end is None:
            raise cs_error.api_request_data_params_invalid
        params = req.RestQueryOrderHistoryReq(symbol, utc_start, utc_end, start_order_no, with_trade, size)
        result_data_json = cns_api.http_post(server_config=self.server_config, api_uri=self.uri.query_order_history,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestQueryOrderHistoryData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 查询历史成交列表
    def query_trade_history(self, symbol, utc_start, utc_end, start_deal_no, size):
        """查询历史成交列表"""
        if is_empty(symbol) or utc_start is None or utc_end is None:
            raise cs_error.api_request_data_params_invalid
        params = req.RestQueryTradeHistoryReq(symbol, utc_start, utc_end, start_deal_no, size)
        result_data_json = cns_api.http_post(server_config=self.server_config,
                                             api_uri=self.uri.query_order_trade_history,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestQueryTradeHistoryData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

    # 查询用户未成交（或未完成）委托单列表
    def query_open_list(self, symbol, num):
        """查询用户未成交（或未完成）委托单列表"""
        if is_empty(symbol) or num is None:
            raise cs_error.api_request_data_params_invalid
        params = req.RestQueryOpenListReq(symbol, num)
        result_data_json = cns_api.http_post(server_config=self.server_config,
                                             api_uri=self.uri.query_order_open_list,
                                             params=cns_api.get_request_data(params, self.coinsuper_auth))
        result_data_bo = resp.RestQueryOpenListData(**result_data_json)
        resp.check_res_the_same(json.dumps(result_data_json), result_data_bo)
        return result_data_bo

