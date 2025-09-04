from flask import request, jsonify
from models import db, Posts, MyUser

def delete_post(post_id):
    """删除帖子"""
    try:
        post = Posts.query.get_or_404(post_id)
        data = request.get_json() or {}
        
        user_id = data.get('user_id')  # 当前用户ID
        is_admin = data.get('is_admin', False)  # 是否为管理员操作
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        # 权限检查：作者或管理员可以删除帖子
        if user_id == post.user:
            # 作者删除自己的帖子
            delete_reason = 'Deleted by author'
        elif is_admin:
            # 验证管理员权限
            admin_user = MyUser.query.get(user_id)
            if not admin_user or not admin_user.admin:
                return jsonify({
                    'success': False,
                    'error': 'Permission denied. Admin access required.'
                }), 403
            delete_reason = f'Deleted by admin: {admin_user.username}'
        else:
            return jsonify({
                'success': False,
                'error': 'Permission denied. Only the author or admin can delete this post.'
            }), 403
        
        # 记录被删除的帖子信息（用于日志）
        post_info = {
            'post_id': post.objectId,
            'author_id': post.user,
            'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
            'delete_reason': delete_reason,
            'deleted_by': user_id
        }
        
        # 删除帖子
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Post deleted successfully',
            'data': post_info
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
