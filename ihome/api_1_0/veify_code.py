# -*- coding:utf8 -*-

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store, constants, db
from flask import current_app, jsonify, make_response, request
from ihome.utils.response_code import RET
from ihome.models import User
from ihome.libs.yuntongxun.sms import CCP
import random
# from ihome.tasks.task_sms_test import send_sms
from ihome.tasks.sms.tasks import send_sms

# GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>

@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :params image_code_id:图片验证编号
    :return: 验证码图片
    """

    # 后端程序的基本套路
    # 1.获取参数 （在这个函数中参数在定义URL中，已经获取了）
    # 2.检验参数  （一般就是校验参数有没有传，这里也不用校验了）
    # 3.业务逻辑处理
    # 4.返回

    ###业务逻辑处理
    # 生成验证码图片
    # 名字，真实文本，图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实编号保存到redis中
    # 将验证码真实值与编号保存到redis中, 设置有效期
    # redis：  字符串   列表  哈希   set
    # "key": xxx
    # 使用哈希维护有效期的时候只能整体设置
    # "image_codes": {"id1":"abc", "":"", "":""} 哈希  hset("image_codes", "id1", "abc")  hget("image_codes", "id1")

    # 单条维护记录，选用字符串
    # "image_code_编号1": "真实值"
    # "image_code_编号2": "真实值"

    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    # 记录名字 ,有效期  ,记录值
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="save image code id failed")

    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


# # GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
# @api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
# def get_sms_code(mobile):
#     """获取短信验证码"""
#     # 获取参数
#     image_code = request.args.get("image_code")
#     image_code_id = request.args.get("image_code_id")
#
#     # 校验参数
#     if not all([image_code, image_code_id]):
#         # 参数不完整
#         return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
#
#     # 业务逻辑处理
#     ## 从redis取出图片验证码
#     try:
#         real_image_code = redis_store.get("image_code_%s" % image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
#
#     # 判断图片验证码是否过期
#     if real_image_code is None:
#         return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
#
#     # 删除redis中图片验证码，防止一个验证码验证多次
#     try:
#         redis_store.delete("image_code_%s" % image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#
#     ## 与用户填写的对比
#     if image_code.lower() != real_image_code.lower():
#         return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
#
#     # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
#     try:
#         send_flag = redis_store.get("send_sms_code_%s" % mobile)
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if send_flag is not None:
#             return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，60秒后在试")
#
#     ## 判断手机号是否注册过
#     try:
#         user = User.query.filter_vy(mobile=mobile).first()
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if user is not None:
#             return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
#
#     ## 生成短信验证码
#     sms_code = "%06d" % random.randint(0, 999999)
#
#     ## 保存真实的短信验证码
#     try:
#         redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#         # 保存该手机号发送短信的记录，防止60秒内再次发送短信
#         redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERAVL, 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="保存验证码异常")
#
#     ## 发送短信
#     try:
#         ccp = CCP()
#         ret = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
#
#     # 返回
#     if ret == 0:
#         return jsonify(errno=RET.OK, errmsg="发送成功")
#     else:
#         return jsonify(errno=RET.THIRDERR, errmsg="发送失败")




# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 校验参数
    if not all([image_code, image_code_id]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理
    ## 从redis取出图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")

    # 判断图片验证码是否过期
    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis中图片验证码，防止一个验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    ## 与用户填写的对比
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，60秒后在试")

    ## 判断手机号是否注册过
    try:
        user = User.query.filter_vy(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    ## 生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)

    ## 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存该手机号发送短信的记录，防止60秒内再次发送短信
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERAVL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存验证码异常")

    ## 发送短信
    # try:
    #     ccp = CCP()
    #     ret = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg="发送异常")

    # 使用celery异步发送短信，delay函数调用后不会堵塞，立即返回
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)



    # 返回
    return jsonify(errno=RET.OK, errmsg="发送成功")