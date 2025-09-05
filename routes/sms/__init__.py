from flask import Blueprint
from .sendsms import send_sms_code
from .verifysms import verify_sms_code

# 创建SMS蓝图
sms_bp = Blueprint('sms', __name__)

# 注册路由
@sms_bp.route('/send', methods=['POST'])
def send_sms():
    """发送短信验证码"""
    return send_sms_code()

@sms_bp.route('/verify', methods=['POST'])
def verify_sms():
    """验证短信验证码"""
    return verify_sms_code()
