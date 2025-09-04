from flask import Blueprint
from .create import create_banner
from .read import get_banners, get_banner, get_active_banners, get_banner_stats
from .update import update_banner, update_banner_sort_order, track_banner_view, track_banner_click
from .delete import delete_banner

# 创建横幅蓝图
banners_bp = Blueprint('banners', __name__)

# 注册路由 - 创建操作
banners_bp.route('/', methods=['POST'])(create_banner)

# 注册路由 - 查询操作
banners_bp.route('/', methods=['GET'])(get_banners)
banners_bp.route('/<string:banner_id>', methods=['GET'])(get_banner)
banners_bp.route('/active', methods=['GET'])(get_active_banners)
banners_bp.route('/stats', methods=['GET'])(get_banner_stats)

# 注册路由 - 更新操作
banners_bp.route('/<string:banner_id>', methods=['PUT'])(update_banner)
banners_bp.route('/<string:banner_id>/sort-order', methods=['POST'])(update_banner_sort_order)
banners_bp.route('/<string:banner_id>/view', methods=['POST'])(track_banner_view)
banners_bp.route('/<string:banner_id>/click', methods=['POST'])(track_banner_click)

# 注册路由 - 删除操作
banners_bp.route('/<string:banner_id>', methods=['DELETE'])(delete_banner)
