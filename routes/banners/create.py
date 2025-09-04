from flask import request, jsonify
from models import db, Banner, MyUser
from datetime import datetime

def create_banner():
    """创建新横幅"""
    try:
        data = request.get_json()
        
        # 检查必需的参数
        title = data.get('title')
        if not title or not title.strip():
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # 验证管理员权限（可选，根据需求决定）
        admin_user_id = data.get('admin_user_id')
        if admin_user_id:
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user or not admin_user.admin:
                return jsonify({
                    'success': False,
                    'error': 'Permission denied. Admin access required.'
                }), 403
        
        # 验证动作类型（可选验证）
        action = data.get('action', '').strip() if data.get('action') else None
        
        # 创建横幅
        banner = Banner(
            title=title.strip(),
            show=data.get('show', True),
            click=data.get('click', True),
            content=data.get('content', '').strip() if data.get('content') else None,
            action=action,
            imageurl=data.get('imageurl', '').strip() if data.get('imageurl') else None,
            sort_order=data.get('sort_order', 0)
        )
        
        db.session.add(banner)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Banner created successfully',
            'data': banner.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
