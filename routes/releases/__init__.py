from flask import Blueprint
from .create import create_release
from .read import get_releases, get_release, get_releases_count
from .update import update_release
from .delete import delete_release
from .upload import upload_apk

# 创建发布版本蓝图
releases_bp = Blueprint('releases', __name__)

# 注册路由 - 创建操作
releases_bp.route('/', methods=['POST'])(create_release)

# 注册路由 - 查询操作
releases_bp.route('/', methods=['GET'])(get_releases)
releases_bp.route('/count', methods=['GET'])(get_releases_count)
releases_bp.route('/<string:object_id>', methods=['GET'])(get_release)

# 注册路由 - 更新操作
releases_bp.route('/<string:object_id>', methods=['PUT'])(update_release)

# 注册路由 - 删除操作
releases_bp.route('/<string:object_id>', methods=['DELETE'])(delete_release)

# 上传 APK
releases_bp.route('/upload-apk', methods=['POST'])(upload_apk)


