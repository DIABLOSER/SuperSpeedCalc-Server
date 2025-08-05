from flask import Blueprint
from .create import create_image, upload_single_image, upload_multiple_images
from .read import get_images, get_image, get_image_stats, search_images
from .update import update_image, update_image_url
from .delete import delete_image, delete_multiple_images, clear_all_images

# 创建图片蓝图
image_bp = Blueprint('image', __name__)

# 注册路由 - 创建操作
image_bp.route('/', methods=['POST'])(create_image)
image_bp.route('/upload', methods=['POST'])(upload_single_image)
image_bp.route('/upload/multiple', methods=['POST'])(upload_multiple_images)

# 注册路由 - 查询操作
image_bp.route('/', methods=['GET'])(get_images)
image_bp.route('/<string:object_id>', methods=['GET'])(get_image)
image_bp.route('/stats', methods=['GET'])(get_image_stats)
image_bp.route('/search', methods=['GET'])(search_images)

# 注册路由 - 更新操作
image_bp.route('/<string:object_id>', methods=['PUT'])(update_image)
image_bp.route('/<string:object_id>/url', methods=['POST'])(update_image_url)

# 注册路由 - 删除操作
image_bp.route('/<string:object_id>', methods=['DELETE'])(delete_image)
image_bp.route('/batch/delete', methods=['POST'])(delete_multiple_images)
image_bp.route('/clear', methods=['DELETE'])(clear_all_images) 