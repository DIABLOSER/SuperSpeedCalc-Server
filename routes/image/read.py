from flask import request, jsonify
from models import db, Image

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
        
        return jsonify({
            'success': True,
            'data': [image.to_dict() for image in images.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': images.total,
                'pages': images.pages
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

#根据 objectId 获取单个图片
def get_image(object_id):
    """根据 objectId 获取单个图片"""
    try:
        image = Image.query.get_or_404(object_id)
        
        return jsonify({
            'success': True,
            'data': image.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

#获取图片统计信息
def get_image_stats():
    """获取图片统计信息"""
    try:
        total_count = Image.query.count()
        total_size = db.session.query(db.func.sum(Image.fileSize)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_images': total_count,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / 1024 / 1024, 2)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

#搜索图片（按文件名）
def search_images():
    """搜索图片（按文件名）"""
    try:
        query_text = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not query_text:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        # 按文件名搜索
        images = Image.query.filter(
            Image.fileName.like(f'%{query_text}%')
        ).order_by(Image.createdAt.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [image.to_dict() for image in images.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': images.total,
                'pages': images.pages
            },
            'search_query': query_text
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 