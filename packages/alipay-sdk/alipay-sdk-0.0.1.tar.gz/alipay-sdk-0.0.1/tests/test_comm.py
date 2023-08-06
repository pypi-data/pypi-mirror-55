#!/usr/bin/python3
# @Time    : 2019-09-12
# @Author  : Kevin Kong (kfx2007@163.com)

from Crypto.PublicKey import RSA
from alipay.comm import Comm
from alipay.api import AliPay
import unittest


class TestComm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestComm, cls).setUpClass()
        with open("private.txt", "r") as f:
            private_key = RSA.importKey(f.read())
        with open("public.txt", "r") as f:
            publick_key = RSA.importKey(f.read())
        cls.alipay = AliPay("2016101100664659", private_key,
                            sign_type="rsa2", ali_public_key=publick_key, sandbox=True)
        cls.alipay_rsa = AliPay(
            "2016101100664659", private_key, ali_public_key=publick_key, sandbox=True)

    def test_sign(self):
        """RSA生成待签名字符"""
        self.api = AliPay("2014072300007148", None, sandbox=True)
        data = {
            "method": "alipay.mobile.public.menu.add",
            "charset": 'GBK',
            "sign_type": 'RSA2',
            "timestamp": '2014-07-24 03:07:50',
            "biz_content": '{"button":[{"actionParam":"ZFB_HFCZ","actionType":"out","name":"话费充值"},{"name":"查询","subButton":[{"actionParam":"ZFB_YECX","actionType":"out","name":"余额查询"},{"actionParam":"ZFB_LLCX","actionType":"out","name":"流量查询"},{"actionParam":"ZFB_HFCX","actionType":"out","name":"话费查询"}]},{"actionParam":"http://m.alipay.com","actionType":"link","name":"最新优惠"}]}',
            "version": "1.0"
        }

        a = self.api.comm.get_signstr(data)
        s = 'app_id=2014072300007148&biz_content={"button":[{"actionParam":"ZFB_HFCZ","actionType":"out","name":"话费充值"},{"name":"查询","subButton":[{"actionParam":"ZFB_YECX","actionType":"out","name":"余额查询"},{"actionParam":"ZFB_LLCX","actionType":"out","name":"流量查询"},{"actionParam":"ZFB_HFCX","actionType":"out","name":"话费查询"}]},{"actionParam":"http://m.alipay.com","actionType":"link","name":"最新优惠"}]}&charset=GBK&method=alipay.mobile.public.menu.add&sign_type=RSA2&timestamp=2014-07-24 03:07:50&version=1.0'
        self.assertEqual(a, s)

    def test_sign_cert(self):
        """RSA证书生成待签名字符"""
        self.api = AliPay("2014072300007148", None, sign_type="rsa_cert", app_cert_sn="50fa7bc5dc305a4fbdbe166689ddc827",
                          alipay_root_cert_sn="6bc29aa3b4d406c43483ffea81e08d22", sandbox=True)
        data = {
            "method": "alipay.mobile.public.menu.add",
            "charset": 'GBK',
            "sign_type": 'RSA2',
            "timestamp": '2014-07-24 03:07:50',
            "biz_content": '{"button":[{"actionParam":"ZFB_HFCZ","actionType":"out","name":"话费充值"},{"name":"查询","subButton":[{"actionParam":"ZFB_YECX","actionType":"out","name":"余额查询"},{"actionParam":"ZFB_LLCX","actionType":"out","name":"流量查询"},{"actionParam":"ZFB_HFCX","actionType":"out","name":"话费查询"}]},{"actionParam":"http://m.alipay.com","actionType":"link","name":"最新优惠"}]}',
            "version": "1.0"
        }
        a = self.api.comm.get_signstr(data)
        s = 'alipay_root_cert_sn=6bc29aa3b4d406c43483ffea81e08d22&app_cert_sn=50fa7bc5dc305a4fbdbe166689ddc827&app_id=2014072300007148&biz_content={"button":[{"actionParam":"ZFB_HFCZ","actionType":"out","name":"话费充值"},{"name":"查询","subButton":[{"actionParam":"ZFB_YECX","actionType":"out","name":"余额查询"},{"actionParam":"ZFB_LLCX","actionType":"out","name":"流量查询"},{"actionParam":"ZFB_HFCX","actionType":"out","name":"话费查询"}]},{"actionParam":"http://m.alipay.com","actionType":"link","name":"最新优惠"}]}&charset=GBK&method=alipay.mobile.public.menu.add&sign_type=RSA2&timestamp=2014-07-24 03:07:50&version=1.0'
        self.assertEqual(a, s)

    def test_sign_rsa(self):
        """RSA验证签名"""
        data = {
            "method": "alipay.mobile.public.menu.add",
            "charset": 'GBK',
            "sign_type": 'RSA',
            "timestamp": '2014-07-24 03:07:50',
            "biz_content": '123',
            "version": "1.0"
        }

        s = self.alipay_rsa.comm.get_signstr(data)
        v_s = "b5UyLbGui7uUSK5bNZrxQO+wjI4XySnjpT9ODpPx0L45886RsPSfFWfTjXYzAkuRKADJrRYpkk41TBsUhhp4dLPJwU6H/R90NZgQ8hIxKn1in0+GK3hDEJOaiO+bEPLGSNAC2iiyAoEBz1llNkP6EQBgBi7JaiNaASBXrh0gFpZ7X8dKlTSsx7jeDYULlxKbS3EXaIZnx3Jnv/LDBjXuaWNjUoc7v8bLHF8LNDsOQ5MxuGdijVY/rOAnNocCCxYCuftErxhGtqCfxuhKdkLJc4+T5+5VejwR8wcUZLk1PYkU6sF7qs6+YfjLUyFFakLVCXx+BpzXrNDbQU49L1vXgA=="
        self.assertEqual(self.alipay_rsa.comm.gen(s), v_s)

    def test_sign_rsa2(self):
        """RSA2签名验证"""

        data = {
            "method": "alipay.mobile.public.menu.add",
            "charset": 'GBK',
            "sign_type": 'RSA2',
            "timestamp": '2014-07-24 03:07:50',
            "biz_content": '123',
            "version": "1.0"
        }

        s = self.alipay.comm.get_signstr(data)
        v_s = "N/ZcddFYAgPCkHQE5GcvK0vqaxYJhTsAvP9E54Kd4iYcGWY6eWwS56UOyHFelCI7ONOhmHKz/vRTndBQngXoQYNq+U+/e/9wrS4uT/4VMWpnivegvooaVYnGgrdWBIseE33G41xlEZZLXnaA0KShC9H6n2vIrP9Jgx93g4mU2S+ExJttY4rtgQJoJXKlXV1a8DHMoXY5flLF6hbLOUzonLpCnwbdU7L2DV5pHkNwkP38iACqbbTqDy6SQyoFrOhkmZAk1J6m79oTB1lmekO56c+FjYPZ+hegEWVwYqM1cpB3JYUDVZ+EBTIUewOq3U+f8CreJkkf3OjI32d3mGFWCg=="
        self.assertEqual(self.alipay.comm.gen(s), v_s)

    def test_validate_sign(self):
        """异步回调验签"""
        data = {
            'gmt_create': '2019-11-06 12:52:18',
            'charset': 'utf-8',
            'gmt_payment': '2019-11-06 12:52:28',
            'notify_time': '2019-11-06 12:52:29',
            'subject': 'SO015-1',
            'sign': 'cG6uWeaX+5FXAJu7O02CI6b8V5L5Qamo/lz3LWvBVNCni4A5G1oWezCOVsqCEII/jO9mErQoY5ZXIW7uayRDOmp4nVWjl9kppDCNdi0YJHTdvY3WfoEUwc6XbDplUWWn9U5X00CPnUIlYMbfWaFFmsW/PVzhECBP2V08iBvbi2pscykf5LtyskG6gorJjzkNUE/WoOw+LV3JR30U8IFbfys7m67HDYRMjbdfSIGVDxZUfNMbgQK0/P3DyDQ0PbmdiD8w/e8WHM29cocJ20jnu8j5ZXyngWw09R/VAAW+15IHWJ+26JLA+vV/IM4Hp+v7C/my0Q+fpQPTcg6QEM/d5w==',
            'buyer_id': '2088102179514385',
            'passback_params': 'return_url%3Dhttp%3A%2F%2Fproject.mixoo.cn%3A80%2Fpayment%2Falipay%2Fvalidate%26reference%3DSO015-1%26amount%3D1.0%26currency%3DCNY%26csrf_token%3D24cc66c330aed25a1bcc9ca07dfbf8fa568327d6o1573019530%26notify_url%3Dhttp%3A%2F%2Fproject.mixoo.cn%3A80%2Fpayment%2Falipay%2Fnotify',
            'invoice_amount': '1.00',
            'version': '1.0',
            'notify_id': '2019110600222125229014381000618776',
            'fund_bill_list': '[{"amount":"1.00","fundChannel":"ALIPAYACCOUNT"}]',
            'notify_type': 'trade_status_sync',
            'out_trade_no': 'SO015-1',
            'total_amount': '1.00',
            'trade_status': 'TRADE_SUCCESS',
            'trade_no': '2019110622001414381000117218',
            'auth_app_id': '2016101100664659',
            'receipt_amount': '1.00',
            'point_amount': '0.00',
            'app_id': '2016101100664659',
            'buyer_pay_amount': '1.00',
            'sign_type': 'RSA2',
            'seller_id': '2088102179155775'
        }

        self.assertTrue(self.alipay.comm.validate_sign(data))


if __name__ == "__main__":
    unittest.main()
