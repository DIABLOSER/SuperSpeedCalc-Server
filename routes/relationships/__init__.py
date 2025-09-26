from flask import Blueprint, request
from .create import follow_user
from .delete import unfollow_user
from .read import get_user_followers, get_user_following, check_follow_relationship, get_mutual_followers

# 创建新的关系蓝图 - 使用改进的路由设计
relationships_bp = Blueprint('relationships', __name__)

# 新的路由设计 - 更简洁、语义更清晰
# 关注操作 - 使用请求体传递参数
relationships_bp.route('/follow', methods=['POST'])(follow_user)
relationships_bp.route('/follow', methods=['DELETE'])(unfollow_user)
relationships_bp.route('/status', methods=['GET'])(check_follow_relationship)

# 关系查询 - 路径参数更清晰
relationships_bp.route('/followers/<string:user_id>', methods=['GET'])(get_user_followers)
relationships_bp.route('/following/<string:user_id>', methods=['GET'])(get_user_following)
relationships_bp.route('/mutual/<string:user_id>', methods=['GET'])(get_mutual_followers)
