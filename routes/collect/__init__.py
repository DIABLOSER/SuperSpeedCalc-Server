from flask import Blueprint
from .create import create_collect
from .read import get_user_collected_posts, get_post_collectors, get_collect_status, get_user_collect_stats
from .delete import delete_collect, delete_collect_by_id, clear_user_collects

# 创建收藏蓝图
collect_bp = Blueprint('collect', __name__)

# 注册路由
collect_bp.add_url_rule('/create', 'create_collect', create_collect, methods=['POST'])
collect_bp.add_url_rule('/user/<user_id>/posts', 'get_user_collected_posts', get_user_collected_posts, methods=['GET'])
collect_bp.add_url_rule('/post/<post_id>/users', 'get_post_collectors', get_post_collectors, methods=['GET'])
collect_bp.add_url_rule('/status/<user_id>/<post_id>', 'get_collect_status', get_collect_status, methods=['GET'])
collect_bp.add_url_rule('/user/<user_id>/stats', 'get_user_collect_stats', get_user_collect_stats, methods=['GET'])
collect_bp.add_url_rule('/delete', 'delete_collect', delete_collect, methods=['POST'])
collect_bp.add_url_rule('/<collect_id>', 'delete_collect_by_id', delete_collect_by_id, methods=['DELETE'])
collect_bp.add_url_rule('/user/<user_id>/clear', 'clear_user_collects', clear_user_collects, methods=['DELETE'])
