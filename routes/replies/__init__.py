from flask import Blueprint, request
from .create import create_reply
from .read import get_post_replies, get_reply, get_user_replies, get_first_level_replies
from .update import update_reply
from .delete import delete_reply

# 创建评论蓝图
replies_bp = Blueprint('replies', __name__)

# 注册路由 - 创建操作
replies_bp.route('/', methods=['POST'])(create_reply)

# 注册路由 - 查询操作
replies_bp.route('/post/<string:post_id>', methods=['GET'])(get_post_replies)
replies_bp.route('/<string:reply_id>', methods=['GET'])(get_reply)
replies_bp.route('/user/<string:user_id>', methods=['GET'])(get_user_replies)
replies_bp.route('/post/<string:post_id>/first-level', methods=['GET'])(get_first_level_replies)
# 兼容性路由 - 支持查询参数方式
replies_bp.route('/', methods=['GET'])(lambda: get_post_replies(request.args.get('post')))

# 注册路由 - 更新操作
replies_bp.route('/<string:reply_id>', methods=['PUT'])(update_reply)

# 注册路由 - 删除操作
replies_bp.route('/<string:reply_id>', methods=['DELETE'])(delete_reply)
