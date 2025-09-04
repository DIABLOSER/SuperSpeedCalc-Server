from flask import request, jsonify
from models import db, Banner, MyUser
from datetime import datetime

def update_banner(banner_id):
    """更新横幅信息"""
    try:
        banner = Banner.query.get_or_404(banner_id)
        data = request.get_json()
        
        # 验证管理员权限（可选）
        admin_user_id = data.get('admin_user_id')
        if admin_user_id:
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user or not admin_user.admin:
                return jsonify({
                    'success': False,
                    'error': 'Permission denied. Admin access required.'
                }), 403
        
        # 更新允许的字段
        if 'title' in data:
            title = data['title'].strip() if data['title'] else ''
            if not title:
                return jsonify({
                    'success': False,
                    'error': 'Title cannot be empty'
                }), 400
            banner.title = title
        
        if 'show' in data:
            banner.show = bool(data['show'])
        
        if 'click' in data:
            banner.click = bool(data['click'])
        
        if 'content' in data:
            banner.content = data['content'].strip() if data['content'] else None
        
        if 'action' in data:
            banner.action = data['action'].strip() if data['action'] else None
        
        if 'imageurl' in data:
            banner.imageurl = data['imageurl'].strip() if data['imageurl'] else None
        
        if 'sort_order' in data:
            banner.sort_order = int(data['sort_order'])
        
        banner.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Banner updated successfully',
            'data': banner.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_banner_sort_order(banner_id):
    """更新横幅排序权重"""
    try:
        banner = Banner.query.get_or_404(banner_id)
        data = request.get_json()
        
        # 验证管理员权限（可选）
        admin_user_id = data.get('admin_user_id')
        if admin_user_id:
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user or not admin_user.admin:
                return jsonify({
                    'success': False,
                    'error': 'Permission denied. Admin access required.'
                }), 403
        
        sort_order = data.get('sort_order')
        if sort_order is None:
            return jsonify({
                'success': False,
                'error': 'sort_order is required'
            }), 400
        
        old_sort_order = banner.sort_order
        banner.sort_order = int(sort_order)
        banner.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Banner sort order updated from {old_sort_order} to {banner.sort_order}',
            'data': {
                'objectId': banner.objectId,
                'title': banner.title,
                'old_sort_order': old_sort_order,
                'new_sort_order': banner.sort_order
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def track_banner_view(banner_id):
    """记录横幅展示（简化版）"""
    try:
        banner = Banner.query.get_or_404(banner_id)
        
        # 检查横幅是否处于活跃状态
        if not banner.is_active():
            return jsonify({
                'success': False,
                'error': 'Banner is not active'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Banner view tracked',
            'data': {
                'banner_id': banner.objectId,
                'title': banner.title
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def track_banner_click(banner_id):
    """记录横幅点击（简化版）"""
    try:
        banner = Banner.query.get_or_404(banner_id)
        
        # 检查横幅是否处于活跃状态且可点击
        if not banner.is_active():
            return jsonify({
                'success': False,
                'error': 'Banner is not active'
            }), 400
        
        if not banner.click:
            return jsonify({
                'success': False,
                'error': 'Banner is not clickable'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Banner click tracked',
            'data': {
                'banner_id': banner.objectId,
                'title': banner.title,
                'action': banner.action
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
