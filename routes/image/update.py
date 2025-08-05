from flask import request, jsonify
from models import db, Image
from datetime import datetime

def update_image(object_id):
    """更新图片信息"""
    try:
        image = Image.query.get_or_404(object_id)
        data = request.get_json()
        
        # 更新允许的字段
        allowed_fields = ['fileName', 'path', 'url', 'fileSize']
        for field in allowed_fields:
            if field in data:
                setattr(image, field, data[field])
        
        image.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': image.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_image_url(object_id):
    """更新图片URL"""
    try:
        image = Image.query.get_or_404(object_id)
        data = request.get_json()
        
        new_url = data.get('url', '')
        if not new_url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
            
        image.url = new_url
        image.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': image.to_dict(),
            'message': 'Image URL updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 