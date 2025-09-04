from flask import Blueprint
from .create import follow_user
from .delete import unfollow_user
from .read import get_user_followers, get_user_following, check_follow_relationship, get_mutual_followers

# 创建关系蓝图
relationship_bp = Blueprint('relationship', __name__)

# 注册路由 - 关注操作
relationship_bp.route('/<string:user_id>/follow/<string:target_user_id>', methods=['POST'])(follow_user)

# 注册路由 - 取消关注操作
relationship_bp.route('/<string:user_id>/follow/<string:target_user_id>', methods=['DELETE'])(unfollow_user)

# 注册路由 - 查询操作
relationship_bp.route('/<string:user_id>/followers', methods=['GET'])(get_user_followers)
relationship_bp.route('/<string:user_id>/following', methods=['GET'])(get_user_following)
relationship_bp.route('/<string:user_id>/mutual', methods=['GET'])(get_mutual_followers)
relationship_bp.route('/<string:user_id>/follow/<string:target_user_id>', methods=['GET'])(check_follow_relationship)
