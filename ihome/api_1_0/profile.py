# -*- coding:utf8 -*-

from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, jsonify, request, session
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import User
from ihome import db, constants


@api.route("/users/avatar", methods=["POST"])
@login_required
def set_user_avatar():
    """设置用户的头像
    参数：图片(多媒体表单格式) 用户ID(g.user_id)
    """
    user_id = g.user_id

    image_file = request.files.get("avatar")
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")

    image_data = image_file.read()
    # 上传图片
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    try:
        User.query.filter_by(id=user_id).update({"avatar_url": file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")

    # 保存成功返回
    avater_url = constants.QINIU_URL_DOMAIN + file_name
    return jsonify(errno=RET.OK, ermsg="上传保存成功", data={"avatar_url": avater_url})


@api.route("/users/name", methods=["PUT"])
@login_required
def change_user_name():
    """修改用户名"""
    user_id = g.user_id
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    name = req_data.get("name")
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="用户名不能为空")

    # 保存用户昵称name，并同时判断name是否重复（利用数据库的唯一索引)
    try:
        User.query.filter_by(id=user_id).update({"name": name})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="设置用户名错误")

    # 修改session数据中的name字段
    session["name"] = name
    return jsonify(errno=RET.OK, errmsg="OK", data={"name": name})


@api.route("/user", methods=["GET"])
@login_required
def get_user_porfile():
    """获取用户个人信息"""
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="操作不成功")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())


@api.route("/users/auth", methods=["GET"])
@login_required
def get_user_auth():
    """获取实名信息"""
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取实名信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="用户获取失败")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


@api.route("/users/auth", methods=["POST"])
@login_required
def set_user_auth():
    """保存实名认证信息"""
    user_id = g.user_id

    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    real_name = req_data.get("real_name")
    id_card = req_data.get("id_card")

    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None).update(
            {"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(erron=RET.DBERR, errmsg="保存实名信息失败")

    return jsonify(errno=RET.OK, errmsg="OK")
