from flask import Blueprint
from .create import create_like
from .read import get_post_likers, get_user_liked_posts, get_like_status, sync_all_post_like_counts
from .update import toggle_like
from .delete import delete_like

# 创建点赞蓝图
likes_bp = Blueprint('likes', __name__)

# 注册路由 - 创建操作
likes_bp.route('/', methods=['POST'])(create_like)

# 注册路由 - 查询操作
likes_bp.route('/post/<string:post_id>/likers', methods=['GET'])(get_post_likers)
likes_bp.route('/user/<string:user_id>/liked', methods=['GET'])(get_user_liked_posts)
likes_bp.route('/status/<string:user_id>/<string:post_id>', methods=['GET'])(get_like_status)
likes_bp.route('/admin/sync-like-counts', methods=['POST'])(sync_all_post_like_counts)

# 注册路由 - 更新操作
likes_bp.route('/toggle', methods=['POST'])(toggle_like)

# 注册路由 - 删除操作
likes_bp.route('/', methods=['DELETE'])(delete_like)
