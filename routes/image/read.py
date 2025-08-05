from flask import request, jsonify
from models import db, Image

def get_images():
    """获取所有图片"""
    try:
        # 支持查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Image.query
        
        # 按创建时间倒序排列
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