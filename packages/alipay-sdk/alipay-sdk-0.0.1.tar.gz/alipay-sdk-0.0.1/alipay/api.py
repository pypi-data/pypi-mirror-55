#!/usr/bin/python3
# @Time    : 2019-09-12
# @Author  : Kevin Kong (kfx2007@163.com)

from alipay.comm import Comm
from alipay.pay import Pay

SANDBOX_URL = "https://openapi.alipaydev.com/gateway.do"
URL = "https://openapi.alipay.com/gateway.do"


class AliPay(object):

    def __init__(self, appid, app_private_key,
                 return_url=None, notify_url=None, ali_public_key=None,
                 sign_type="rsa", app_cert_sn=None, alipay_root_cert_sn=None,
                 sandbox=False):
        """
        初始化API
        参数：
        appid: 应用id
        app_private_key: 商户密钥
        app_cert_sn: 应用公钥证书SN
        alipay_root_cert_sn: 支付宝根证书SN
        sign_type: 签名方式(rsa和rsa2两种)
        公钥证书方式下，应用公钥和支付宝证书SN 必填
        """
        self.appid = appid
        self.url = SANDBOX_URL if sandbox else URL
        self.app_private_key = app_private_key
        self.ali_public_key = ali_public_key
        self.sign_type = sign_type.upper()
        self.app_cert_sn = app_cert_sn
        self.alipay_root_cert_sn = alipay_root_cert_sn
        self.return_url = return_url
        self.notify_url = notify_url

    comm = Comm()
    pay = Pay()
