from flask import jsonify, request
from models import MyUser

def get_users():
    """获取所有用户（支持排序与分页）"""
    try:
        # 排序参数
        sort_by = request.args.get('sort_by')
        order = (request.args.get('order') or 'asc').lower()

        # 分页参数（手动 limit/offset）
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 10, 1), 100)

        # 允许排序的字段白名单
        allowed_fields = {
            'username': MyUser.username,
            'email': MyUser.email,
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

def get_users_count():
    """获取用户总数"""
    try:
        total = MyUser.query.count()
        return jsonify({'success': True, 'data': {'total_users': total}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 