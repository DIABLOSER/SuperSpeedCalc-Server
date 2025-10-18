from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import AppRelease
from sqlalchemy import desc


def get_releases():
    """获取发布记录列表（可筛选 title、environment）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        title = request.args.get('title')
        environment = request.args.get('environment')

        query = AppRelease.query
        if title:
            query = query.filter(AppRelease.title == title)
        if environment:
            query = query.filter(AppRelease.environment == environment)

        query = query.order_by(desc(AppRelease.createdAt))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = [x.to_dict() for x in pagination.items]

        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
        return paginated_response(
            items=items,
            pagination=pagination_info,
            message='获取发布记录成功'
        )
    except Exception as e:
        return internal_error_response(
            message='获取失败',
        )


def get_release(object_id):
    try:
        item = AppRelease.query.get(object_id)
        if not item:
            return not_found_response(
                message='发布记录不存在',
                # error_code='RELEASE_NOT_FOUND'
            )
        return success_response(
            data=item.to_dict(),
            message='获取成功'
        )
    except Exception as e:
        return internal_error_response(
            message='获取失败',
        )


def get_releases_count():
    try:
        title = request.args.get('title')
        environment = request.args.get('environment')

        query = AppRelease.query
        if title:
            query = query.filter(AppRelease.title == title)
        if environment:
            query = query.filter(AppRelease.environment == environment)

        return success_response(
            data={'count': query.count()},
            message='获取数量成功'
        )
    except Exception as e:
        return internal_error_response(
            message='获取失败',
        )

def get_latest_release():
    """
    根据环境和是否更新获取最新版本
    
    查询参数:
        environment: 发布环境（例如：测试、taptap、正式）
        is_update: 是否更新（true/false）
    """
    try:
        # 获取查询参数
        environment = request.args.get('environment')
        is_update = request.args.get('is_update')
        
        # 参数验证
        if not environment:
            return bad_request_response(message='缺少必需参数：environment')
        
        if is_update is None:
            return bad_request_response(message='缺少必需参数：is_update')
        
        # 转换 is_update 参数为布尔值
        try:
            is_update_bool = is_update.lower() in ['true', '1', 'yes', 'on']
        except AttributeError:
            return bad_request_response(message='is_update 参数格式错误，应为 true/false')
        
        # 构建查询
        query = AppRelease.query.filter(
            AppRelease.environment == environment,
            AppRelease.is_update == is_update_bool
        ).order_by(desc(AppRelease.createdAt))
        
        # 获取最新记录
        item = query.first()
        
        # 检查是否找到数据
        if not item:
            return not_found_response(
                message=f'未找到环境为 {environment} 且更新状态为 {is_update} 的发布记录'
            )
        
        return success_response(
            data=item.to_dict(),
            message='获取最新版本成功'
        )
        
    except Exception as e:
        # 记录详细错误信息用于调试
        print(f"获取最新版本失败: {str(e)}")
        return internal_error_response(
            message='获取最新版本失败，请稍后重试'
        )