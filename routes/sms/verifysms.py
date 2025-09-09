from flask import request, jsonify, current_app
from models import db, Reply, MyUser, Posts
from datetime import datetime
from bmobpy import Bmob
from utils.response import (
    success_response, bad_request_response, internal_error_response
)


def verify_sms_code():
    """验证短信验证码"""
    try:
        # 添加详细日志
        current_app.logger.info("=" * 50)
        current_app.logger.info("🔍 开始处理短信验证请求")
        current_app.logger.info(f"请求方法: {request.method}")
        current_app.logger.info(f"请求URL: {request.url}")
        current_app.logger.info(f"请求头: {dict(request.headers)}")
        current_app.logger.info(f"请求数据: {request.get_json()}")
        current_app.logger.info(f"客户端IP: {request.remote_addr}")
        current_app.logger.info(f"用户代理: {request.headers.get('User-Agent', 'Unknown')}")
        
        data = request.get_json()
        # 支持多种字段名：phone 和 phone_number
        phone = data.get('phone') or data.get('phone_number')
        # 支持多种验证码字段名：code 和 verification_code
        code = data.get('code') or data.get('verification_code')
        
        current_app.logger.info(f"提取的手机号: {phone}")
        current_app.logger.info(f"提取的验证码: {code}")
        current_app.logger.info(f"原始请求数据: {data}")
        current_app.logger.info(f"数据字段检查 - phone: {data.get('phone')}, phone_number: {data.get('phone_number')}, code: {data.get('code')}, verification_code: {data.get('verification_code')}")
        
        if not phone:
            current_app.logger.warning("❌ 手机号为空")
            return bad_request_response(
                message='手机号是必需的，请使用 phone 或 phone_number 字段',
                # error_code='MISSING_PHONE'
            )
        
        if not code:
            current_app.logger.warning("❌ 验证码为空")
            return bad_request_response(
                message='验证码是必需的，请使用 code 或 verification_code 字段',
                # error_code='MISSING_VERIFICATION_CODE'
            )
        
        # 验证手机号格式（简单验证）
        current_app.logger.info(f"开始验证手机号格式: {phone}")
        current_app.logger.info(f"手机号长度: {len(phone) if phone else 0}")
        current_app.logger.info(f"手机号是否为数字: {phone.isdigit() if phone else False}")
        
        if not phone.isdigit() or len(phone) != 11:
            current_app.logger.warning(f"❌ 手机号格式不正确: {phone} (长度: {len(phone) if phone else 0}, 是否数字: {phone.isdigit() if phone else False})")
            return bad_request_response(
                message='手机号格式不正确',
                # error_code='INVALID_PHONE_FORMAT'
            )
        
        current_app.logger.info(f"✅ 手机号格式验证通过: {phone}")
        
        # 验证验证码格式（简单验证）
        current_app.logger.info(f"开始验证验证码格式: {code}")
        current_app.logger.info(f"验证码长度: {len(code) if code else 0}")
        current_app.logger.info(f"验证码是否为数字: {code.isdigit() if code else False}")
        
        if not code.isdigit() or len(code) != 6:
            current_app.logger.warning(f"❌ 验证码格式不正确: {code} (长度: {len(code) if code else 0}, 是否数字: {code.isdigit() if code else False})")
            return bad_request_response(
                message='验证码格式不正确',
                # error_code='INVALID_VERIFICATION_CODE_FORMAT'
            )
        
        current_app.logger.info(f"✅ 验证码格式验证通过: {code}")
        
        # 初始化Bmob
        current_app.logger.info("🔧 开始初始化Bmob")
        current_app.logger.info(f"BMOB_APPLICATION_ID: {current_app.config.get('BMOB_APPLICATION_ID', 'Not Set')[:10]}...")
        current_app.logger.info(f"BMOB_REST_API_KEY: {current_app.config.get('BMOB_REST_API_KEY', 'Not Set')[:10]}...")
        
        bmob = Bmob(
            current_app.config['BMOB_APPLICATION_ID'],
            current_app.config['BMOB_REST_API_KEY']
        )
        current_app.logger.info("✅ Bmob对象创建成功")
        
        # 设置Master Key（如果需要更高权限）
        if current_app.config.get('BMOB_MASTER_KEY'):
            current_app.logger.info("🔑 设置Bmob Master Key")
            current_app.logger.info(f"BMOB_MASTER_KEY: {current_app.config.get('BMOB_MASTER_KEY', 'Not Set')[:10]}...")
            bmob.setMasterKey(current_app.config['BMOB_MASTER_KEY'])
            current_app.logger.info("✅ Master Key设置成功")
        else:
            current_app.logger.info("ℹ️  未设置Master Key")
        
        # 验证短信验证码
        current_app.logger.info(f"🔍 开始验证短信验证码")
        current_app.logger.info(f"调用方法: bmob.verifySmsCode('{phone}', '{code}')")
        
        result = bmob.verifySmsCode(phone, code)
        current_app.logger.info(f"📋 Bmob验证结果: {result}")
        current_app.logger.info(f"结果类型: {type(result)}")
        
        if result:
            current_app.logger.info("✅ 短信验证码验证成功")
            current_app.logger.info("=" * 50)
            return success_response(
                data={
                    'phone': phone,
                    'verified': True
                },
                message='短信验证码验证成功'
            )
        else:
            # 获取错误信息
            error_msg = bmob.getError() if hasattr(bmob, 'getError') else '验证失败'
            current_app.logger.warning(f"❌ 短信验证码验证失败: {error_msg}")
            current_app.logger.info("=" * 50)
            return bad_request_response(
                message=f'短信验证码验证失败: {error_msg}',
                # error_code='SMS_VERIFICATION_FAILED'
            )
            
    except Exception as e:
        import traceback
        current_app.logger.error(f"💥 验证短信验证码异常: {str(e)}")
        current_app.logger.error(f"异常类型: {type(e).__name__}")
        current_app.logger.error(f"异常详情: {traceback.format_exc()}")
        current_app.logger.error("=" * 50)
        return internal_error_response(
            message=f'服务器内部错误: {str(e)}',
            # error_code='SMS_VERIFICATION_SERVICE_ERROR'
        )