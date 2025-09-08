from flask import jsonify, request
from models import MyUser
from sqlalchemy import or_
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response
)

#获取所有用户
def get_users():
    """获取所有用户（支持排序、分页、模糊搜索）"""
    try:
        # 排序参数
        sort_by = request.args.get('sort_by')
        order = (request.args.get('order') or 'asc').lower()

        # 分页参数（手动 limit/offset）
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 10, 1), 100)

        # 搜索关键词（对 username、email、mobile 模糊匹配）
        keyword = (request.args.get('keyword') or request.args.get('q') or '').strip()

        # 允许排序的字段白名单
        allowed_fields = {
            'username': MyUser.username,
            'email': MyUser.email,
            'mobile': MyUser.mobile,
            'experience': MyUser.experience,
            'boluo': MyUser.boluo,
            'isActive': MyUser.isActive,
            'admin': MyUser.admin,
            'sex': MyUser.sex,
            'birthday': MyUser.birthday,
            'createdAt': MyUser.createdAt,
            'updatedAt': MyUser.updatedAt,
        }

        query = MyUser.query

        # 根据用户名、手机号、邮箱进行模糊匹配
        if keyword:
            pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    MyUser.username.ilike(pattern),
                    MyUser.email.ilike(pattern),
                    MyUser.mobile.ilike(pattern)
                )
            )

        if sort_by in allowed_fields:
            col = allowed_fields[sort_by]
            query = query.order_by(col.desc() if order == 'desc' else col.asc())

        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1

        return paginated_response(
            data=[u.to_dict() for u in items],
            page=page,
            per_page=per_page,
            total=total,
            message="获取用户列表成功"
        )
    except Exception as e:
        return internal_error_response(
            message="获取用户列表失败",
            error_code="GET_USERS_FAILED",
            details=str(e)
        )
#根据用户名、手机号、邮箱进行模糊匹配

#根据用户Id获取用户信息
def get_user(object_id):
    """根据 objectId 获取单个用户"""
    try:
        user = MyUser.query.get_or_404(object_id)
        return success_response(
            data=user.to_dict(),
            message="获取用户信息成功"
        )
    except Exception as e:
        return not_found_response(
            message="用户不存在",
            error_code="USER_NOT_FOUND",
            details=str(e)
        )

#获取用户总数
def get_users_count():
    """获取用户总数"""
    try:
        total = MyUser.query.count()
        return success_response(
            data={'total_users': total},
            message="获取用户总数成功"
        )
    except Exception as e:
        return internal_error_response(
            message="获取用户总数失败",
            error_code="GET_USERS_COUNT_FAILED",
            details=str(e)
        ) 