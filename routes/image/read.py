from flask import request, jsonify
from models import db, Image
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response
)

#支持排序和分页获取所有图片
def get_images():
    """获取所有图片（支持排序与分页）"""
    try:
        # 查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        sort_by = request.args.get('sort_by')
        order = (request.args.get('order') or 'desc').lower()
        
        query = Image.query
        
        # 允许排序的字段白名单
        allowed_fields = {
            'fileName': Image.fileName,
            'fileSize': Image.fileSize,
            'createdAt': Image.createdAt,
            'updatedAt': Image.updatedAt,
        }
        
        # 应用排序：默认按创建时间倒序
        if sort_by in allowed_fields:
            col = allowed_fields[sort_by]
            query = query.order_by(col.desc() if order == 'desc' else col.asc())
        else:
            query = query.order_by(Image.createdAt.desc())
        
        # 分页
        images = query.paginate(page=page, per_page=per_page, error_out=False)
        
        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": images.total,
            "pages": images.pages,
            "has_next": images.has_next,
            "has_prev": images.has_prev
        }
        return paginated_response(
            items=[image.to_dict() for image in images.items],
            pagination=pagination_info,
            message="获取图片列表成功"
        )
    except Exception as e:
        return internal_error_response(
            message="获取图片列表失败",
        )

#根据 objectId 获取单个图片
def get_image(object_id):
    """根据 objectId 获取单个图片"""
    try:
        image = Image.query.get_or_404(object_id)
        
        return success_response(
            data=image.to_dict(),
            message="获取图片信息成功"
        )
    except Exception as e:
        return not_found_response(
            message="图片不存在",
            # error_code="IMAGE_NOT_FOUND"
        )

#获取图片统计信息
def get_image_stats():
    """获取图片统计信息"""
    try:
        total_count = Image.query.count()
        total_size = db.session.query(db.func.sum(Image.fileSize)).scalar() or 0
        
        return success_response(
            data={
                'total_images': total_count,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / 1024 / 1024, 2)
            },
            message="获取图片统计信息成功"
        )
    except Exception as e:
        return internal_error_response(
            message="获取图片统计信息失败",
            # error_code="GET_IMAGE_STATS_FAILED"
        )

#搜索图片（按文件名）
def search_images():
    """搜索图片（按文件名）"""
    try:
        query_text = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not query_text:
            from utils.response import bad_request_response
            return bad_request_response(
                message="搜索关键词是必需的",
                # error_code="MISSING_SEARCH_QUERY"
            )
        
        # 按文件名搜索
        images = Image.query.filter(
            Image.fileName.like(f'%{query_text}%')
        ).order_by(Image.createdAt.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return success_response(
            data={
                'images': [image.to_dict() for image in images.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': images.total,
                    'pages': images.pages
                },
                'search_query': query_text
            },
            message="搜索图片成功"
        )
    except Exception as e:
        return internal_error_response(
            message="搜索图片失败",
            # error_code="SEARCH_IMAGES_FAILED"
        ) 