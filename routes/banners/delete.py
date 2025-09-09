from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Banner, MyUser

def delete_banner(banner_id):
    """删除横幅"""
    try:
        banner = Banner.query.get_or_404(banner_id)
        data = request.get_json() or {}
        
        # 验证管理员权限（可选）
        admin_user_id = data.get('admin_user_id')
        if admin_user_id:
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user or not admin_user.admin:
                return internal_error_response(message='Permission denied. Admin access required.', code=403)
        
        # 记录被删除的横幅信息
        banner_info = {
            'banner_id': banner.objectId,
            'title': banner.title,
            'show': banner.show,
            'click': banner.click,
            'deleted_by': admin_user_id if admin_user_id else 'system'
        }
        
        # 删除横幅
        db.session.delete(banner)
        db.session.commit()
        
        return created_response(data=banner_info, message='Banner deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
