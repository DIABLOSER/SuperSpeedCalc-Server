from flask import Blueprint
from .create import feedback_create_bp
from .read import feedback_read_bp
from .update import feedback_update_bp
from .delete import feedback_delete_bp

# 创建反馈模块蓝图
feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/feedback')

# 注册子蓝图
feedback_bp.register_blueprint(feedback_create_bp)
feedback_bp.register_blueprint(feedback_read_bp)
feedback_bp.register_blueprint(feedback_update_bp)
feedback_bp.register_blueprint(feedback_delete_bp)
