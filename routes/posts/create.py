from flask import request, jsonify
from models import db, Posts, MyUser
from datetime import datetime

def create_post():
    """创建新帖子"""
    try:
        data = request.get_json()
        
        # 检查必需的参数
        user_id = data.get('user')
        content = data.get('content')
        
        if not user_id or not content:
            return jsonify({
                'success': False,
                'error': 'User ID and content are required'
            }), 400
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # 检查内容长度
        if len(content.strip()) == 0:
            return jsonify({
                'success': False,
                'error': 'Content cannot be empty'
            }), 400
        
        # 创建帖子
        post = Posts(
            user=user_id,
            content=content.strip(),
            visible=data.get('visible', True),
            audit_state=data.get('audit_state', 'pending')
        )
        
        # 处理图片列表
        images = data.get('images', [])
        if isinstance(images, list):
            post.set_images_list(images)
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Post created successfully',
            'data': post.to_dict(include_author=True, user_id=user_id)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
