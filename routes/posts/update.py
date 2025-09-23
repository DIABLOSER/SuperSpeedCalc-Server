from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Posts, MyUser, Likes
from datetime import datetime

def update_post(post_id):
    """更新帖子信息（包括审核状态）"""
    try:
        post = Posts.query.get_or_404(post_id)
        data = request.get_json()
        
        # 移除权限检查，任何人都可以更新帖子
        user_id = data.get('user_id')  # 当前用户ID
        
        # 更新允许的字段
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return internal_error_response(message='Content cannot be empty', code=400)
            post.content = content
        
        if 'visible' in data:
            post.visible = bool(data['visible'])
        
        if 'images' in data:
            images = data['images']
            if isinstance(images, list):
                post.set_images_list(images)
        
        # 更新审核状态
        if 'audit_state' in data:
            new_audit_state = data['audit_state']
            reason = data.get('reason', '')  # 审核意见
            
            # 验证审核状态
            valid_states = Posts.get_audit_states()
            if new_audit_state not in valid_states:
                return bad_request_response(
                    message=f'Invalid audit state. Valid states: {list(valid_states.keys())}',
                    code=400
                )
            
            old_state = post.audit_state
            post.audit_state = new_audit_state
        
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return updated_response(data=post.to_dict(include_user=True, user_id=user_id), message='Post updated successfully')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)


