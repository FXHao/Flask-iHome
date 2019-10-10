# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf07086d62068d016d824bee071a09'

# 主帐号Token
accountToken = '6bebe43e918b4baba1df336e8d6e3bac'

# 应用Id
appId = '8aaf07086d62068d016d824bee581a10'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class CCP(object):
    """自己封装的发送短信的辅助类"""
    # 用来保存对象实例属性
    instance = None

    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建并保存一个对象，有则保存对象直接返回
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj

        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        """"""
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
        # smsMessageSid:4
        # dcc6ecdb38b46f7a4b8a39583101c8d
        # dateCreated:20191001152906
        # statusCode:000000
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功
            return 0
        else:
            # 发送失败
            return -1
