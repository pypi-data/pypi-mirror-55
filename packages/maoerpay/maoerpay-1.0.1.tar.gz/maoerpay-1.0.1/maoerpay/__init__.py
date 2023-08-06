# coding: utf-8

from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA

import json
import requests
from urllib.parse import quote
from base64 import encodebytes

class MaoerPay(object):
    def __init__(
            self,
            mch_id = "",
            PRIVATE_KEY = ""
    ):
        self.__mch_id = mch_id
        self.__app_private_key = RSA.importKey(PRIVATE_KEY)
        self.__api_url = "https://open.maoer.net.cn/api/trade/"

    def __sign(self, unsigned_string):
        # 开始计算签名
        key = self.__app_private_key
        signer = PKCS1_v1_5.new(key)
        data = self.__b(unsigned_string)
        # return data
        signature = signer.sign(SHA256.new(data))

        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def __b(self,s):
        return s.encode("utf-8")

    def __add_data(self, data):
        complex_keys = [k for k, v in data.items() if isinstance(v, dict)]

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def __build_query(self,data):
        data.pop("sign", None)
        data['mchid'] = self.__mch_id
        # 字典型转数组并排序
        ordered_items = self.__add_data(data)
        # 将数组拼接成Key=Value格式
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in ordered_items)
        sign = self.__sign(unsigned_string)

        # 获得最终的订单信息字符串
        signed_string = unsigned_string + "&sign=" + quote(sign)
        return signed_string

    def __http(self,function,post_data = ""):
        f = requests.post(function,post_data)
        return f.text

    def barpay(self,data):
        params = self.__build_query(data)
        return self.__http(self.__api_url + "barpay",params)

    def jspay(self,data):
        if data['trade_type'] == 'JSAPI' and 'openid' not in data:
            return 'JSAPI支付时，openid为必传参数'
        if data['trade_type'] == 'NATIVE' and 'product_id' not in data:
            return 'NATIVE支付时，product_id为必传参数'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "jspay",params)

    def order_query(self,data):
        if 'out_trade_no' not in data and 'maoer_id' not in data:
            return 'out_trade_no和maoer_id不能同时为空'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "order_query",params)

    def order_close(self,data):
        if 'out_trade_no' not in data:
            return '请传递要关闭的订单号'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "order_close",params)

    def order_reverse(self,data):
        if 'out_trade_no' not in data:
            return '请传递要撤销的订单号'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "order_reverse",params)

    def refund(self,data):
        if 'refund_desc' not in data:
            data['refund_desc'] = '正常退款'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "refund",params)

    def refund_query(self,data):
        if 'out_refund_no' not in data:
            return '请传递要要查询的退款单号'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "refund_query",params)

    def downloadbill(self,data):
        if 'bill_date' not in data and 'bill_type' not in data:
            return '必填参数不全'
        params = self.__build_query(data)
        return self.__http(self.__api_url + "downloadbill",params)