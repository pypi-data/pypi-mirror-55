#!/usr/bin/python3
# @Time    : 2019-10-31
# @Author  : Kevin Kong (kfx2007@163.com)

# 支付宝当面付
# 包含 条码支付、扫码支付两个业务场景

from alipay.comm import Comm, isp_args
import inspect


class Pay(Comm):

    @isp_args
    def trade_create(self, out_trade_no, total_amount, subject,
                     body=None, buyer_id=None, discountable_amount=None, seller_id=None,
                     goods_detail=None, product_code=None, operator_id=None, store_id=None, terminal_id=None,
                     extend_params=None, timeout_express=None, settle_info=None, logistics_detail=None, business_params=None,
                     receiver_address_info=None):
        """
        统一收单交易创建接口
        """
        return self.post()

    @isp_args
    def trade_pay(self, out_trade_no, scene, auth_code, subject,
                  product_code=None, buyer_id=None, seller_id=None,
                  total_amount=None, trans_currency=None, settle_currency=None,
                  discountable_amount=None, body=None, goods_detail=None,
                  operator_id=None, store_id=None, terminal_id=None,
                  extend_params=None, timeout_express=None, auth_confirm_mode=None,
                  terminal_params=None, promo_params=None, advance_payment_type=None):
        """
        统一收单交易支付接口
        参数：
            out_trade_no: string 商户订单号 64个字符以内
            scene： string 支付场景 (bar_code,wave_code) 32 
            auth_code: string 支付授权码 32 
            subject: string 订单标题 32
            product_code: string 产品码 32
            buyer_id: string 买家支付宝id 28
            seller_id: string 卖家支付宝id 28
            total_amount: float 订单总金额 11 
            trans_currency: string 币种
            settle_currency: string 商户结算币种
            discountable_amount：float 参与优惠计算的金额，单位为元，精确到小数点后两位
            body: string 订单描述
            goods_detail: list 订单包含的商品列表信息，json格式
            operator_id: string 商户操作员编号
            store_id: string 商户门店编号
            terminal_id: string 商户机具终端编号
            extend_params: dict 业务扩展参数
            timeout_express: string 该笔订单允许的最晚付款时间，逾期将关闭交易。
            auth_confirm_mode: string 预授权确认模式，授权转交易请求中传入，适用于预授权转交易业务使用，目前只支持PRE_AUTH(预授权产品码)
            terminal_params: 商户传入终端设备相关信息，具体值要和支付宝约定
            promo_params: 优惠明细参数，通过此属性补充营销参数
            advance_payment_type: 支付模式类型,若值为ENJOY_PAY_V2表示当前交易允许走先享后付2.0垫资
        """
        return self.post()

    @isp_args
    def trade_close(self, trade_no=None, out_trade_no=None, operator_id=None):
        """
        统一收单交易关闭接口
        参数：
            trade_no： string 64 该交易在支付宝系统中的交易流水号
            out_trade_no: string 64 订单支付时传入的商户订单号,和支付宝交易号不能同时为空
            operator_id: 卖家端自定义的的操作员 ID
        """
        if not trade_no and not out_trade_no:
            raise Exception("交易流水号和商户订单号不能同时为空")
        return self.post()

    @isp_args
    def trade_query(self, out_trade_no=None, trade_no=None, org_pid=None, query_options=None):
        """
        统一收单线下交易查询
        参数：
            out_trade_no：string 订单支付时传入的商户订单号,和支付宝交易号不能同时为空。
            trade_no：string 支付宝交易号，和商户订单号不能同时为空
            org_pid：string 银行间联模式下有用，其它场景请不要使用
            query_options： string 查询选项，商户通过上送该字段来定制查询返回信息
        """
        if not trade_no and not out_trade_no:
            raise Exception("交易流水号和商户订单号不能同时为空")
        return self.post()

    @isp_args
    def trade_refund(self, refund_amount, out_trade_no=None, trade_no=None,
                     refund_currency=None, refund_reason=None, out_request_no=None,
                     operator_id=None, store_id=None, terminal_id=None, goods_detail=None,
                     refund_royalty_parameters=None):
        """
        统一收单交易退款接口
        参数：
            refund_amount: float 需要退款的金额，该金额不能大于订单金额,单位为元，支持两位小数 
            out_trade_no： string 64 订单支付时传入的商户订单号,不能和 trade_no同时为空
            trade_no： string   64 支付宝交易号，和商户订单号不能同时为空
            refund_currency: string 8 订单退款币种信息
            refund_reason: string 256  退款的原因说明
            out_request_no: string 64 标识一次退款请求，同一笔交易多次退款需要保证唯一，如需部分退款，则此参数必传
            operator_id: string 30 商户的操作员编号
            store_id: string 32 商户的门店编号
            terminal_id: string 32 商户的终端编号
            goods_detail: list 退款包含的商品列表信息，Json格式。其它说明详见 https://docs.open.alipay.com/api_1/alipay.trade.refund
            refund_royalty_parameters: dict 退分账明细信息
            org_pid: string 16 银行间联模式下有用，其它场景请不要使用；双联通过该参数指定需要退款的交易所属收单机构的pid;
        """
        if not trade_no and not out_trade_no:
            raise Exception("支付宝交易号，和商户订单号不能同时为空")
        return self.post()

    @isp_args
    def trade_fastpay_refund_query(self, out_request_no, trade_no=None, out_trade_no=None, org_pid=None):
        """
        统一收单交易退款查询
        参数：
            trade_no: string 64 支付宝交易号，和商户订单号不能同时为空
            out_trade_no:  string 64 订单支付时传入的商户订单号,和支付宝交易号不能同时为空
            out_request_no: string 64 请求退款接口时，传入的退款请求号，如果在退款请求时未传入，则该值为创建交易时的外部交易号
            org_pid: string 16 银行间联模式下有用，其它场景请不要使用；双联通过该参数指定需要退款的交易所属收单机构的pid;
        """
        if not trade_no and not out_trade_no:
            raise Exception("支付宝交易号，和商户订单号不能同时为空")
        return self.post()

    @isp_args
    def trade_precreate(self, out_trade_no, total_amount, subject,
                        goods_detail=None, discountable_amount=None,
                        seller_id=None, body=None, product_code=None,
                        operator_id=None, store_id=None, disable_pay_channels=None,
                        enable_pay_channels=None, terminal_id=None, extend_params=None,
                        timeout_express=None, settle_info=None, merchant_order_no=None,
                        business_params=None, qr_code_timeout_express=None):
        """
        统一收单线下交易预创建
        收银员通过收银台或商户后台调用支付宝接口，生成二维码后，展示给用户，由用户扫描二维码完成订单支付。
        参数：
            out_trade_no: string 64 商户订单号,64个字符以内、只能包含字母、数字、下划线；需保证在商户端不重复
            total_amount: float 订单总金额，单位为元，精确到小数点后两位
            subject: string 256 订单标题
            goods_detail: list 订单包含的商品列表信息.json格式. 其它说明详见：“商品明细说明”
            discountable_amount: float 可打折金额. 参与优惠计算的金额，单位为元，精确到小数点后两位
            seller_id: string 28 卖家支付宝用户ID。 如果该值为空，则默认为商户签约账号对应的支付宝用户ID
            body: string 128 对交易或商品的描述
            product_code: 销售产品码。
            operator_id: 商户操作员编号
            store_id: 商户门店编号
            disable_pay_channels:禁用渠道，用户不可用指定渠道支付当有多个渠道时用“,”分隔注，与enable_pay_channels互斥渠道列表：https://docs.open.alipay.com/common/wifww7
            enable_pay_channels: string 128 可用渠道，用户只能在指定渠道范围内支付当有多个渠道时用“,”分隔注，与disable_pay_channels互斥渠道列表
            terminal_id: string 32 商户机具终端编号
            extend_params: dict 业务扩展参数 详细信息参考 https://docs.open.alipay.com/api_1/alipay.trade.precreate/
            timeout_express: string 32 该笔订单允许的最晚付款时间，逾期将关闭交易。取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。 该参数数值不接受小数点， 如 1.5h，可转换为 90m
            settle_info: json 描述结算信息，json格式，详见结算参数说明
            merchant_order_no: string 32 商户原始订单号，最大长度限制32位
            business_params: json 商户传入业务信息，具体值要和支付宝约定，应用于安全，营销等参数直传场景，格式为json格式
            qr_code_timeout_express: string 6 该笔订单允许的最晚付款时间，逾期将关闭交易，从生成二维码开始计时。取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。 该参数数值不接受小数点， 如 1.5h，可转换为 90m。
        """
        return self.post()

    @isp_args
    def trade_cancel(self, out_trade_no=None, trade_no=None):
        """
        支付交易返回失败或支付系统超时，调用该接口撤销交易。
        如果此订单用户支付失败，支付宝系统会将此订单关闭；
        如果用户支付成功，支付宝系统会将此订单资金退还给用户。 
        注意：只有发生支付系统超时或者支付结果未知时可调用撤销，其他正常支付的单如需实现相同功能请调用申请退款API。
        提交支付交易后调用【查询订单API】，没有明确的支付结果再调用【撤销订单API】
        """
        if not trade_no and not out_trade_no:
            raise Exception("支付宝交易号，和商户订单号不能同时为空")
        return self.post()

    @isp_args
    def trade_page_pay(self, out_trade_no, total_amount, subject, product_code="FAST_INSTANT_TRADE_PAY",
                       body=None, time_expire=None, goods_detail=None, passback_params=None, extend_params=None,
                       goods_type=None, timeout_express=None, promo_params=None, royalty_info=None, sub_merchant=None,
                       merchant_order_no=None, enable_pay_channels=None, store_id=None, disable_pay_channels=None,
                       qr_pay_mode=None, qrcode_width=None, settle_info=None, invoice_info=None,
                       agreement_sign_params=None, integration_type=None, request_from_url=None,
                       business_params=None, ext_user_info=None):
        """
        统一收单下单并支付页面接口
        参数：
            out_trade_no: string 64 商户订单号,64个字符以内、可包含字母、数字、下划线
            total_amount: float 订单总金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
            subject: string 256 订单标题
            product_code: string 64 销售产品码，与支付宝签约的产品码名称。注：目前仅支持FAST_INSTANT_TRADE_PAY
            body: string 128 订单描述
            time_expire： string 32 绝对超时时间，格式为yyyy-MM-dd HH:mm:ss
            goods_detail: list 订单包含的商品列表信息，json格式，其它说明详见商品明细说明
            passback_params: string 512 公用回传参数，如果请求时传递了该参数，则返回给商户时会回传该参数。支付宝只会在同步返回（包括跳转回商户网站）和异步通知时将该参数原样返回。本参数必须进行UrlEncode之后才可以发送给支付宝
            extend_params: dict 业务扩展参数
            goods_type: string 2 商品主类型 :0-虚拟类商品,1-实物类商品 注：虚拟类商品不支持使用花呗渠道
            timeout_express: string 6 该笔订单允许的最晚付款时间，逾期将关闭交易。取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。 该参数数值不接受小数点， 如 1.5h，可转换为 90m
            promo_params: string 512 优惠参数 注：仅与支付宝协商后可用
            royalty_info: json 描述分账信息，json格式，详见分账参数说明
            sub_merchant: json 间连受理商户信息体，当前只对特殊银行机构特定场景下使用此字段
            merchant_order_no: string 32 商户原始订单号，最大长度限制32位
            enable_pay_channels: string 128 可用渠道,用户只能在指定渠道范围内支付，多个渠道以逗号分割 注，与disable_pay_channels互斥 渠道列表：https://docs.open.alipay.com/common/wifww7 
            store_id: string 32 商户门店编号
            disable_pay_channels: string 128 禁用渠道,用户不可用指定渠道支付，多个渠道以逗号分割 注，与enable_pay_channels互斥
            qr_pay_mode: string 2 PC扫码支付的方式，支持前置模式和跳转模式。
                0：订单码-简约前置模式，对应 iframe 宽度不能小于600px，高度不能小于300px；
                1：订单码-前置模式，对应iframe 宽度不能小于 300px，高度不能小于600px；
                2：订单码-跳转模式
                3：订单码-迷你前置模式，对应 iframe 宽度不能小于 75px，高度不能小于75px；
                4：订单码-可定义宽度的嵌入式二维码，商户可根据需要设定二维码的大小。
            qrcode_width: int 商户自定义二维码宽度 注：qr_pay_mode=4时该参数生效
            settle_info: json 描述结算信息，json格式，详见结算参数说明
            invoice_info: json 开票信息	
            agreement_sign_params: 签约参数，支付后签约场景使用
            integration_type: string 16 请求后页面的集成方式。取值范围：1. ALIAPP：支付宝钱包内 2. PCWEB：PC端访问
            request_from_url: string 256 请求来源地址。如果使用ALIAPP的集成方式，用户中途取消支付会返回该地址。
            business_params: string 512 商户传入业务信息，具体值要和支付宝约定，应用于安全，营销等参数直传场景，格式为json格式
            ext_user_info: json 外部指定买家
        返回：
            拼接好的URL,由应用程序直接发起请求即可
        """
        return self._get_request_url()
