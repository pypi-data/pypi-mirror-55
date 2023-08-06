#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import logging
import time
import unittest
import uuid

import coinsuper.rest.coinsuper_rest as coinsuper
import coinsuper.rest.cns_api as cns_api
import coinsuper.rest.logger.coinsuper_simple_log as log
import coinsuper.rest.error.coinsuper_rest_error as cs_error
import json

# str = "a".join(["a", "b", "c"])
# logger.info(str)
from coinsuper.rest.vo.external.req_bo import RestPlaceBatchOrderParam
from coinsuper.rest.vo.internal.req_bo import RestRequestKlineRange

log.is_print_only = False
log.set_node_level(logging.DEBUG)


class CoinsuperRestTest(unittest.TestCase):
    rest = coinsuper.CoinsuperRest("zhangsan", "zhangsan")
    rest.server_config = cns_api.CoinsuperServerConfig("https", "apisandbox.coinsuper.info", "443")

    # self.rest.server_config = cns_api.CoinsuperServerConfig.create_default()

    def setUp(self):
        log.info("开始测试")

    def tearDown(self):
        log.info("测试结束")

    @staticmethod
    def print_bo(result_bo):
        log.info(json.dumps(result_bo, default=lambda obj: obj.__dict__, sort_keys=True))

    # 获取用户账户信息
    def test_query_asset_info(self):
        try:
            log.info("获取用户账户信息")
            result_bo = self.rest.query_asset_info(["BTC", "USD"])
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 获取订单薄行情
    def test_get_market_order_book(self):
        try:
            log.info("获取订单薄行情")
            result_bo = self.rest.get_market_order_book(symbol="BTC/USD", num=1)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 获取K线行情
    def test_get_market_kline(self):
        try:
            log.info("获取K线行情")
            result_bo = self.rest.get_market_kline(symbol="BTC/USD", num=1, range=RestRequestKlineRange.RANGE_5MIN)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 获取最新成交行情
    def test_get_market_tickers(self):
        try:
            log.info("获取最新成交行情")
            result_bo = self.rest.get_market_tickers(symbol="BTC/USD")
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 获取可交易的交易对列表
    def test_get_symbol_list(self):
        try:
            log.info("获取可交易的交易对列表")
            result_bo = self.rest.get_symbol_list()
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 下限价买单
    def test_place_buy_limit_order(self):
        try:
            log.info("下限价买单")
            symbol = "BTC/USD"
            price_limit = "123.45"
            quantity = "0.1234"
            client_order_id = str(uuid.uuid4())
            result_bo = self.rest.place_buy_limit_order(symbol, price_limit, quantity, client_order_id)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 下市价买单
    def test_place_buy_market_order(self):
        try:
            log.info("下市价买单")
            symbol = "BTC/USD"
            amount = "0.01"
            client_order_id = str(uuid.uuid4())
            result_bo = self.rest.place_buy_market_order(symbol, amount, client_order_id)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 下限价卖单
    def test_place_sell_limit_order(self):
        try:
            log.info("下限价卖单")
            symbol = "BTC/USD"
            price_limit = "123.45"
            quantity = "0.1234"
            client_order_id = str(uuid.uuid4())
            result_bo = self.rest.place_sell_limit_order(symbol, price_limit, quantity, client_order_id)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 下限价卖单
    def test_place_sell_market_order(self):
        try:
            log.info("下限价卖单")
            symbol = "BTC/USD"
            quantity = "0.1234"
            client_order_id = str(uuid.uuid4())
            result_bo = self.rest.place_sell_market_order(symbol, quantity, client_order_id)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 取消委托
    def test_cancel_order(self):
        try:
            log.info("取消委托")
            order_no = "1647546849123811329"
            result_bo = self.rest.cancel_order(order_no)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 下批量买单
    def test_place_batch_buy_order(self):
        try:
            log.info("下批量买单")
            symbol = "BTC/USD"
            price_limit = "123.45"
            quantity = "0.1234"
            amount = "10"
            client_order_id1 = str(uuid.uuid4())
            client_order_id2 = str(uuid.uuid4())
            buy_limit_order = RestPlaceBatchOrderParam.create_buy_limit_order(price_limit, quantity, client_order_id1)
            buy_market_order = RestPlaceBatchOrderParam.create_buy_market_order(amount, client_order_id2)

            result_bo = self.rest.place_batch_buy_order(symbol, [buy_limit_order, buy_market_order])
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 下批量卖单
    def test_place_batch_sell_order(self):
        try:
            log.info("下批量卖单")
            symbol = "BTC/USD"
            price_limit = "123.45"
            quantity = "0.1234"
            client_order_id1 = str(uuid.uuid4())
            client_order_id2 = str(uuid.uuid4())
            buy_limit_order = RestPlaceBatchOrderParam.create_sell_limit_order(price_limit, quantity, client_order_id1)
            buy_market_order = RestPlaceBatchOrderParam.create_sell_market_order(quantity, client_order_id2)

            result_bo = self.rest.place_batch_sell_order(symbol, [buy_limit_order, buy_market_order])
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 批量取消委托--根据Coinsuper委托单号列表
    def test_batch_cancel_order_by_order_no_list(self):
        try:
            log.info("批量取消委托--根据Coinsuper委托单号列表")
            order_no_list = ["1647609226028568578", "1647609226028568579"]

            result_bo = self.rest.batch_cancel_order_by_order_no_list(order_no_list)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 批量取消委托--根据客户端订单id列表
    def test_batch_cancel_order_by_client_order_id_list(self):
        try:
            log.info("批量取消委托--根据客户端订单id列表")
            client_order_id_list = ["0baf51a9-68a7-4603-8aa6-f8d0325d447d", "6e56f661-1642-47fd-bebb-d24ec317f649"]

            result_bo = self.rest.batch_cancel_order_by_client_order_id_list(client_order_id_list)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 查询委托列表--根据Coinsuper委托单号列表
    def test_query_order_list_by_order_no_list(self):
        try:
            log.info("查询委托列表--根据Coinsuper委托单号列表")
            order_no_list = ["1647609226028568578", "1647609226028568579"]

            result_bo = self.rest.query_order_list_by_order_no_list(order_no_list)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 查询委托列表--根据客户端订单id列表
    def test_query_order_list_by_client_order_id_list(self):
        try:
            log.info("查询委托列表--根据客户端订单id列表")
            client_order_id_list = ["0baf51a9-68a7-4603-8aa6-f8d0325d447d", "6e56f661-1642-47fd-bebb-d24ec317f649"]

            result_bo = self.rest.query_order_list_by_client_order_id_list(client_order_id_list)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 查询订单交易详情--根据Coinsuper委托单号列表
    def test_query_order_details_by_order_no_list(self):
        try:
            log.info("查询订单交易详情--根据Coinsuper委托单号列表")
            order_no_list = ["1647609226028568578", "1647609226028568579"]

            result_bo = self.rest.query_order_details_by_order_no_list(order_no_list)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 查询历史委托单列表
    def test_query_order_history(self):
        try:
            log.info("查询历史委托单列表")
            symbol = "BTC/USD"
            t = time.time()
            utc_end = int(round(t * 1000))
            utc_start = utc_end - 1 * 24 * 60 * 60 * 1000

            result_bo = self.rest.query_order_history(symbol, utc_start, utc_end, start_order_no=None,
                                                      with_trade="true", size=None)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 查询历史委托单列表
    def test_query_trade_history(self):
        try:
            log.info("查询历史委托单列表")
            symbol = "BTC/USD"
            t = time.time()
            utc_end = int(round(t * 1000))
            utc_start = utc_end - 1 * 24 * 60 * 60 * 1000

            result_bo = self.rest.query_trade_history(symbol, utc_start, utc_end, None, None)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)

    # 查询用户未成交（或未完成）委托单列表
    def test_query_open_list(self):
        try:
            log.info("查询用户未成交（或未完成）委托单列表")
            symbol = "BTC/USD"
            num = 10

            result_bo = self.rest.query_open_list(symbol, num)
            self.print_bo(result_bo)
        except cs_error.CoinsuperRestApiError as err:
            log.error("API server warning: {}", err)


if __name__ == '__main__':
    unittest.main()
