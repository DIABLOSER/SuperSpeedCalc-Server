from flask import request, jsonify
from models import db, Forum, MyUser

def create_forum_post():
    """创建新的社区帖子"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['content', 'user']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        # 验证作者是否存在
        author = MyUser.query.get(data['user'])
        if not author:
            return jsonify({'success': False, 'error': 'Author not found'}), 404
        
        # 创建新帖子
        post = Forum(
            content=data['content'],
            category=data.get('category'),
            tags=data.get('tags', []),
            public=data.get('public', True),
            images=data.get('images', []),
            user=data['user']
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': post.to_dict(include_user=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 