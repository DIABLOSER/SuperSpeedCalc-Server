from flask import request, jsonify, current_app
from models import db, Reply, MyUser, Posts
from datetime import datetime
from bmobpy import Bmob
from utils.response import (
    success_response, bad_request_response, internal_error_response
)


def send_sms_code():
    """发送短信验证码"""
    try:
        # 添加详细日志
        current_app.logger.info(f"收到短信发送请求: {request.get_json()}")
        
        data = request.get_json()
        # 支持两种字段名：phone 和 phone_number
        phone = data.get('phone') or data.get('phone_number')
        
        current_app.logger.info(f"提取的手机号: {phone}")
        current_app.logger.info(f"原始请求数据: {data}")
        
        if not phone:
            current_app.logger.warning("手机号为空")
            return bad_request_response(
                message='手机号是必需的，请使用 phone 或 phone_number 字段',
                error_code='MISSING_PHONE'
            )
        
        # 验证手机号格式（简单验证）
        if not phone.isdigit() or len(phone) != 11:
            current_app.logger.warning(f"手机号格式不正确: {phone}")
            return bad_request_response(
                message='手机号格式不正确',
                error_code='INVALID_PHONE_FORMAT'
            )
        
        # 初始化Bmob
        current_app.logger.info("开始初始化Bmob")
        bmob = Bmob(
            current_app.config['BMOB_APPLICATION_ID'],
            current_app.config['BMOB_REST_API_KEY']
        )
        
        # 设置Master Key（如果需要更高权限）
        if current_app.config.get('BMOB_MASTER_KEY'):
            current_app.logger.info("设置Bmob Master Key")
            bmob.setMasterKey(current_app.config['BMOB_MASTER_KEY'])
        
        # 发送短信验证码
        current_app.logger.info(f"开始发送短信验证码到: {phone}")
        result = bmob.requestSMSCode(phone)
        current_app.logger.info(f"Bmob发送结果: {result}")
        
        if result:
            current_app.logger.info(f"短信发送成功: {phone}")
            return success_response(
                data={'phone': phone},
                message='短信验证码发送成功'
            )
        else:
            # 获取错误信息
            error_msg = bmob.getError() if hasattr(bmob, 'getError') else '发送失败'
            current_app.logger.error(f"短信发送失败: {error_msg}")
            return internal_error_response(
                message=f'短信验证码发送失败: {error_msg}',
                error_code='SMS_SEND_FAILED'
            )
            
    except Exception as e:
        current_app.logger.error(f"发送短信验证码异常: {str(e)}")
        return internal_error_response(
            message=f'服务器内部错误: {str(e)}',
            error_code='SMS_SERVICE_ERROR',
            details=str(e)
        )