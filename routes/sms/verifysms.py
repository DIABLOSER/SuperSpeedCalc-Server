from flask import request, jsonify, current_app
from models import db, Reply, MyUser, Posts
from datetime import datetime
from bmobpy import Bmob


def verify_sms_code():
    """验证短信验证码"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        code = data.get('code')
        
        if not phone:
            return jsonify({'success': False, 'error': '手机号是必需的'}), 400
        
        if not code:
            return jsonify({'success': False, 'error': '验证码是必需的'}), 400
        
        # 验证手机号格式（简单验证）
        if not phone.isdigit() or len(phone) != 11:
            return jsonify({'success': False, 'error': '手机号格式不正确'}), 400
        
        # 验证验证码格式（简单验证）
        if not code.isdigit() or len(code) != 6:
            return jsonify({'success': False, 'error': '验证码格式不正确'}), 400
        
        # 初始化Bmob
        bmob = Bmob(
            current_app.config['BMOB_APPLICATION_ID'],
            current_app.config['BMOB_REST_API_KEY']
        )
        
        # 设置Master Key（如果需要更高权限）
        if current_app.config.get('BMOB_MASTER_KEY'):
            bmob.setMasterKey(current_app.config['BMOB_MASTER_KEY'])
        
        # 验证短信验证码
        result = bmob.verifySmsCode(phone, code)
        
        if result:
            return jsonify({
                'success': True,
                'message': '短信验证码验证成功',
                'phone': phone,
                'verified': True
            }), 200
        else:
            # 获取错误信息
            error_msg = bmob.getError() if hasattr(bmob, 'getError') else '验证失败'
            return jsonify({
                'success': False,
                'error': f'短信验证码验证失败: {error_msg}'
            }), 400
            
    except Exception as e:
        current_app.logger.error(f"验证短信验证码异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        }), 500