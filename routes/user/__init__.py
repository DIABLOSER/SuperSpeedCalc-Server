from flask import Blueprint
from .create import create_user, register_user, login
from .read import get_users, get_user, get_users_count
from .update import update_user, update_user_score, update_user_experence, update_user_boluo
from .delete import delete_user

# 创建用户蓝图
user_bp = Blueprint('user', __name__)

# 注册路由 - 创建操作
user_bp.route('/', methods=['POST'])(create_user)
user_bp.route('/register', methods=['POST'])(register_user)
user_bp.route('/login', methods=['POST'])(login)

# 注册路由 - 查询操作
user_bp.route('/', methods=['GET'])(get_users)
user_bp.route('/count', methods=['GET'])(get_users_count)
user_bp.route('/<string:object_id>', methods=['GET'])(get_user)

# 注册路由 - 更新操作
user_bp.route('/<string:object_id>', methods=['PUT'])(update_user)
user_bp.route('/<string:object_id>/score', methods=['POST'])(update_user_score)
user_bp.route('/<string:object_id>/experence', methods=['POST'])(update_user_experence)
user_bp.route('/<string:object_id>/boluo', methods=['POST'])(update_user_boluo)

# 注册路由 - 删除操作
user_bp.route('/<string:object_id>', methods=['DELETE'])(delete_user) 