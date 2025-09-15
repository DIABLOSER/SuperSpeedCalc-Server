from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, AppRelease


def create_release():
    """创建应用发布记录"""
    try:
        data = request.get_json() or {}

        # 校验 version_code 类型（如果提供）

        release = AppRelease(
            title=data.get('title').strip() if data.get('title') else None,
            version_name=data.get('version_name'),
            version_code=data.get('version_code'),
            content=data.get('content'),
            download_url=data.get('download_url'),
            environment=data.get('environment'),
            is_test=bool(data.get('is_test', False)),
            is_update=bool(data.get('is_update', False)),
            force_update=bool(data.get('force_update', False)),
        )

        db.session.add(release)
        db.session.commit()

        return created_response(
            data=release.to_dict(),
            message='发布记录创建成功'
        )
    except Exception as e:
        db.session.rollback()
        return internal_error_response(
            message='创建失败',
            # error_code='RELEASE_CREATE_FAILED'
        )

        


