from flask import Blueprint
from .create import create_chart
from .read import get_charts, get_chart, get_leaderboard
from .update import update_chart, update_achievement
from .delete import delete_chart

# 创建图表蓝图
charts_bp = Blueprint('charts', __name__)

# 注册路由 - 创建操作
charts_bp.route('/', methods=['POST'])(create_chart)

# 注册路由 - 查询操作
charts_bp.route('/', methods=['GET'])(get_charts)
charts_bp.route('/<string:object_id>', methods=['GET'])(get_chart)
charts_bp.route('/leaderboard', methods=['GET'])(get_leaderboard)

# 注册路由 - 更新操作
charts_bp.route('/<string:object_id>', methods=['PUT'])(update_chart)
charts_bp.route('/<string:object_id>/achievement', methods=['POST'])(update_achievement)

# 注册路由 - 删除操作
charts_bp.route('/<string:object_id>', methods=['DELETE'])(delete_chart) 