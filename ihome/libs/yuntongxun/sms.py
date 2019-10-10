# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf07086d62068d016d824bee071a09'

# ���ʺ�Token
accountToken = '6bebe43e918b4baba1df336e8d6e3bac'

# Ӧ��Id
appId = '8aaf07086d62068d016d824bee581a10'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

class CCP(object):
    """�Լ���װ�ķ��Ͷ��ŵĸ�����"""
    # �����������ʵ������
    instance = None

    def __new__(cls):
        # �ж�CCP����û���Ѿ������õĶ������û�У�����������һ���������򱣴����ֱ�ӷ���
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            # ��ʼ��REST SDK
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
            # ��ʾ���Ͷ��ųɹ�
            return 0
        else:
            # ����ʧ��
            return -1
