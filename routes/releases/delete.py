from flask import jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, AppRelease


def delete_release(object_id):
    try:
        item = AppRelease.query.get(object_id)
        if not item:
            return not_found_response(
                message='发布记录不存在',
                # error_code='RELEASE_NOT_FOUND'
            )

        db.session.delete(item)
        db.session.commit()
        return deleted_response(message='删除成功')
    except Exception as e:
        db.session.rollback()
        return internal_error_response(
            message='删除失败',
            # error_code='RELEASE_DELETE_FAILED'
        )


