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
        
        # 记录被删除的横幅信息
        banner_info = {
            'banner_id': banner.objectId,
            'title': banner.title,
            'show': banner.show,
            'click': banner.click,
            'action': banner.action
        }
        
        # 删除横幅
        db.session.delete(banner)
        db.session.commit()
        
        return deleted_response(data=banner_info, message='Banner deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
