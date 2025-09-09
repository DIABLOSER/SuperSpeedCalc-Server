from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import AppRelease
from sqlalchemy import desc


def get_releases():
    """获取发布记录列表（可筛选 app_name、environment、status）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        app_name = request.args.get('app_name')
        environment = request.args.get('environment')
        status = request.args.get('status')

        query = AppRelease.query
        if app_name:
            query = query.filter(AppRelease.app_name == app_name)
        if environment:
            query = query.filter(AppRelease.environment == environment)
        if status:
            query = query.filter(AppRelease.status == status)

        query = query.order_by(desc(AppRelease.createdAt))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = [x.to_dict() for x in pagination.items]

        return paginated_response(
            data=items,
            page=page,
            per_page=per_page,
            total=pagination.total,
            message='获取发布记录成功'
        )
    except Exception as e:
        return internal_error_response(
            message='获取失败',
            error_code='RELEASE_GET_FAILED',
            details=str(e)
        )


def get_release(object_id):
    try:
        item = AppRelease.query.get(object_id)
        if not item:
            return not_found_response(
                message='发布记录不存在',
                error_code='RELEASE_NOT_FOUND'
            )
        return success_response(
            data=item.to_dict(),
            message='获取成功'
        )
    except Exception as e:
        return internal_error_response(
            message='获取失败',
            error_code='RELEASE_GET_FAILED',
            details=str(e)
        )


def get_releases_count():
    try:
        app_name = request.args.get('app_name')
        environment = request.args.get('environment')
        status = request.args.get('status')

        query = AppRelease.query
        if app_name:
            query = query.filter(AppRelease.app_name == app_name)
        if environment:
            query = query.filter(AppRelease.environment == environment)
        if status:
            query = query.filter(AppRelease.status == status)

        return success_response(
            data={'count': query.count()},
            message='获取数量成功'
        )
    except Exception as e:
        return internal_error_response(
            message='获取失败',
            error_code='RELEASE_GET_FAILED',
            details=str(e)
        )


