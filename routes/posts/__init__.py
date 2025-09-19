from flask import Blueprint
from .create import create_post
from .read import get_posts, get_post, get_user_posts, get_posts_by_audit_state
from .update import update_post, like_post, unlike_post
from .delete import delete_post
from .likes import get_post_likers, get_user_liked_posts, sync_all_post_like_counts

# 创建帖子蓝图
posts_bp = Blueprint('posts', __name__)

# 注册路由 - 创建操作
posts_bp.route('/', methods=['POST'])(create_post)

# 注册路由 - 查询操作
posts_bp.route('/', methods=['GET'])(get_posts)
posts_bp.route('/<string:post_id>', methods=['GET'])(get_post)
posts_bp.route('/user/<string:user_id>', methods=['GET'])(get_user_posts)
posts_bp.route('/audit/<string:audit_state>', methods=['GET'])(get_posts_by_audit_state)

# 注册路由 - 更新操作
posts_bp.route('/<string:post_id>', methods=['PUT'])(update_post)
posts_bp.route('/<string:post_id>/like', methods=['POST'])(like_post)
posts_bp.route('/<string:post_id>/like', methods=['DELETE'])(unlike_post)

# 注册路由 - 点赞查询操作
posts_bp.route('/<string:post_id>/likers', methods=['GET'])(get_post_likers)
posts_bp.route('/user/<string:user_id>/liked', methods=['GET'])(get_user_liked_posts)
posts_bp.route('/admin/sync-like-counts', methods=['POST'])(sync_all_post_like_counts)

# 注册路由 - 删除操作
posts_bp.route('/<string:post_id>', methods=['DELETE'])(delete_post)
