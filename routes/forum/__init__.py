from flask import Blueprint
from .create import create_forum_post
from .read import get_forum_posts, get_forum_post, get_categories, get_popular_posts, get_public_posts
from .update import update_forum_post, like_forum_post
from .delete import delete_forum_post

# 创建论坛蓝图
forum_bp = Blueprint('forum', __name__)

# 注册路由 - 创建操作
forum_bp.route('/', methods=['POST'])(create_forum_post)

# 注册路由 - 查询操作
forum_bp.route('/', methods=['GET'])(get_forum_posts)
forum_bp.route('/<string:object_id>', methods=['GET'])(get_forum_post)
forum_bp.route('/categories', methods=['GET'])(get_categories)
forum_bp.route('/popular', methods=['GET'])(get_popular_posts)
forum_bp.route('/public', methods=['GET'])(get_public_posts)

# 注册路由 - 更新操作
forum_bp.route('/<string:object_id>', methods=['PUT'])(update_forum_post)
forum_bp.route('/<string:object_id>/like', methods=['POST'])(like_forum_post)

# 注册路由 - 删除操作
forum_bp.route('/<string:object_id>', methods=['DELETE'])(delete_forum_post) 