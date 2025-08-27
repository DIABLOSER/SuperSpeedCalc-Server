from flask import Blueprint
from .create import create_history
from .read import get_histories, get_history, get_histories_count, get_score_leaderboard, get_user_score_stats
from .update import update_history
from .delete import delete_history

# 创建历史记录蓝图
history_bp = Blueprint('history', __name__)

# 注册路由 - 创建操作
history_bp.route('/', methods=['POST'])(create_history)

# 注册路由 - 查询操作
history_bp.route('/', methods=['GET'])(get_histories)
history_bp.route('/count', methods=['GET'])(get_histories_count)
history_bp.route('/<string:object_id>', methods=['GET'])(get_history)
history_bp.route('/leaderboard', methods=['GET'])(get_score_leaderboard)
history_bp.route('/stats', methods=['GET'])(get_user_score_stats)

# 注册路由 - 更新操作
history_bp.route('/<string:object_id>', methods=['PUT'])(update_history)

# 注册路由 - 删除操作
history_bp.route('/<string:object_id>', methods=['DELETE'])(delete_history)
