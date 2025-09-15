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

        required_fields = ['title', 'version_name', 'version_code']
        for field in required_fields:
            if data.get(field) in [None, '']:
                return bad_request_response(
                    message=f'{field} 不能为空',
                    # error_code='MISSING_REQUIRED_FIELD',
                    # details={'field': field}
                )

        # 校验类型
        try:
            version_code = int(data.get('version_code'))
        except Exception:
            return bad_request_response(
                message='version_code 必须是整数',
                # error_code='INVALID_VERSION_CODE'
            )

        release = AppRelease(
            title=str(data.get('title')).strip(),
            version_name=str(data.get('version_name')).strip(),
            version_code=version_code,
            content=data.get('content'),
            download_url=data.get('download_url'),
            environment=(data.get('environment') or 'production'),
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

        


