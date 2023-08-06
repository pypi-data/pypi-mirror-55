#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from coinsuper.rest.coinsuper_constant import RestRequestOrderType


class RestPlaceBatchOrderParam:
    """
    Coinsuper API REST批量下单入参
    注：
    1. 若orderType=MKT, action=BUY, 则priceLimit和quantity传入"0", amount为用户输入值；
    2. 若其它情况, 则priceLimit和quantity为用户输入值, amount为"0"；
    3. 此处签名方式请注意：签名方式为将data作为key，整个value数组当做一个字符串处理；
    4. 下单单次最多支持100笔单，且仅限同1个交易对，同1种买卖类型
    """
    def __init__(self, priceLimit, orderType, quantity, amount, clientOrderId):
        self.priceLimit = priceLimit
        self.orderType = orderType
        self.quantity = quantity
        self.amount = amount
        self.clientOrderId = clientOrderId

    @classmethod
    def create_buy_limit_order(cls, priceLimit, quantity, clientOrderId):
        """创建一个限价买单参数"""
        return cls(priceLimit, RestRequestOrderType.LMT, quantity, "0", clientOrderId)

    @classmethod
    def create_sell_limit_order(cls, priceLimit, quantity, clientOrderId):
        """创建一个限价卖单参数"""
        return cls(priceLimit, RestRequestOrderType.LMT, quantity, "0", clientOrderId)

    @classmethod
    def create_buy_market_order(cls, amount, clientOrderId):
        """创建一个市价买单参数"""
        return cls("0", RestRequestOrderType.MKT, "0", amount, clientOrderId)

    @classmethod
    def create_sell_market_order(cls, quantity, clientOrderId):
        """创建一个市价卖单参数"""
        return cls("0", RestRequestOrderType.MKT, quantity, "0", clientOrderId)


