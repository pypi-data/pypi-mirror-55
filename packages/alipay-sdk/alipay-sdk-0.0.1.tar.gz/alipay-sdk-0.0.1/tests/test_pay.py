#!/usr/bin/python3
# @Time    : 2019-10-31
# @Author  : Kevin Kong (kfx2007@163.com)

import unittest
from Crypto.PublicKey import RSA
from alipay.api import AliPay
from autils.string import String
import time


class TestPay(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPay, cls).setUpClass()
        with open("private.txt", "r") as f:
            private_key = RSA.importKey(f.read())
        cls.alipay = AliPay("2016101100664659", private_key,
                            sign_type="rsa2", sandbox=True)
        cls.buyer_id = "2088102179514385"
        cls.order_no = String.generate_digits(24)
        print(f"测试订单：{cls.order_no}")

    def test_trade_create(self):
        """测试统一下单"""
        # 测试不存在的用户
        res = self.alipay.pay.trade_create(
            self.order_no, 1.01, "测试统一下单", buyer_id="208810217951438X", product_code="FACE_TO_FACE_PAYMENT")
        self.assertEqual(res["code"], "40004")

        res = self.alipay.pay.trade_create(
            self.order_no, 2.00, "测试统一下单", buyer_id=self.buyer_id, product_code="FACE_TO_FACE_PAYMENT")
        self.assertEqual(res['code'], '10000')

    def test_trade_pay(self):
        """测试扫码付款"""
        # 收款码错误
        res = self.alipay.pay.trade_pay(
            String.generate_digits(24), "bar_code", "28091756689709104X", "测试中文支付", total_amount=2)
        self.assertEqual(res["code"], '40004')

    def test_trade_close(self):
        """测试统一收单关闭接口"""
        # 测试关闭订单
        # 支付宝沙箱环境总是返回20000
        res = self.alipay.pay.trade_close(
            out_trade_no="190507823711243775320439")
        self.assertIn(res["code"], ['10000', '20000'], msg=res)

    def test_trade_query(self):
        """统一收单线下交易查询"""
        res = self.alipay.pay.trade_query(self.order_no)
        self.assertEqual(res["code"], "10000")

    def test_trade_refund(self):
        """测试统一收单交易退款接口"""
        # 收款后状态才能退款，因此接口总是返回40004
        res = self.alipay.pay.trade_refund(1, out_trade_no=self.order_no)
        self.assertEqual(res["code"], "40004", res)

    def test_trade_refund_query(self):
        """测试统一收单退款查询"""
        res = self.alipay.pay.trade_fastpay_refund_query(
            self.order_no, out_trade_no=self.order_no)
        self.assertEqual(res["code"], "10000", msg=res)

    def test_precreate(self):
        """统一收单线下交易预创建"""
        res = self.alipay.pay.trade_precreate(
            String.generate_digits(24), 1.00, "测试预创建")
        # 沙箱接口一定几率返回None
        if res:
            self.assertEqual(res["code"], "10000", msg=res)

    def test_trade_page_pay(self):
        """测试统一下单并支付页面接口"""
        # 接口返回的是URL连接，因此不报错即认为测试通过
        res = self.alipay.pay.trade_page_pay(
            "SO123", 10, "测试", product_code="FAST_INSTANT_TRADE_PAY")
        self.assertTrue(res)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestPay("test_trade_create"))
    suite.addTest(TestPay("test_trade_close"))
    # suite.addTest(TestPay("test_trade_query"))
    # suite.addTest(TestPay("test_trade_refund"))
    # suite.addTest(TestPay("test_precreate"))
    # suite.addTest(TestPay("test_trade_page_pay"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
