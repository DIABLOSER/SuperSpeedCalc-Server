from flask import jsonify
from models import db, MyUser
from utils.response import (
    deleted_response, not_found_response, internal_error_response
)

def delete_user(object_id):
    """删除用户"""
    try:
        user = MyUser.query.get_or_404(object_id)
        db.session.delete(user)
        db.session.commit()
        
        return deleted_response(message="用户删除成功")
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="删除用户失败") 