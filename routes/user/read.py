from flask import jsonify, request
from models import MyUser
from sqlalchemy import or_

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
            'score': MyUser.score,
            'experence': MyUser.experence,
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

        return jsonify({
            'success': True,
            'data': [u.to_dict() for u in items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
#根据用户名、手机号、邮箱进行模糊匹配

#根据用户Id获取用户信息
def get_user(object_id):
    """根据 objectId 获取单个用户"""
    try:
        user = MyUser.query.get_or_404(object_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

#获取用户总数
def get_users_count():
    """获取用户总数"""
    try:
        total = MyUser.query.count()
        return jsonify({'success': True, 'data': {'total_users': total}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 