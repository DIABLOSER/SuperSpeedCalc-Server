from flask import jsonify, request
from models import Posts, MyUser
from sqlalchemy import desc, and_, or_

def get_posts():
    """获取帖子列表（支持排序、分页、筛选）"""
    try:
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 排序参数
        sort_by = request.args.get('sort_by', 'createdAt')
        order = (request.args.get('order') or 'desc').lower()
        
        # 筛选参数
        visible_only = request.args.get('visible_only', 'true').lower() == 'true'
        approved_only = request.args.get('approved_only', 'true').lower() == 'true'
        user_id = request.args.get('user_id')  # 当前查看用户的ID
        
        # 搜索关键词
        keyword = (request.args.get('keyword') or '').strip()
        
        # 允许排序的字段
        allowed_fields = {
            'createdAt': Posts.createdAt,
            'updatedAt': Posts.updatedAt,
            'likeCount': Posts.likeCount,
            'replyCount': Posts.replyCount
        }
        
        query = Posts.query
        
        # 应用可见性筛选
        if visible_only or approved_only:
            conditions = []
            
            if visible_only:
                if user_id:
                    # 对于已登录用户：显示公开的帖子 + 自己的所有帖子
                    conditions.append(
                        or_(Posts.visible == True, Posts.user == user_id)
                    )
                else:
                    # 对于未登录用户：只显示公开的帖子
                    conditions.append(Posts.visible == True)
            
            if approved_only:
                if user_id:
                    # 对于已登录用户：显示已审核的帖子 + 自己的所有帖子
                    conditions.append(
                        or_(Posts.audit_state == 'approved', Posts.user == user_id)
                    )
                else:
                    # 对于未登录用户：只显示已审核的帖子
                    conditions.append(Posts.audit_state == 'approved')
            
            if conditions:
                query = query.filter(and_(*conditions))
        
        # 关键词搜索
        if keyword:
            query = query.filter(Posts.content.ilike(f'%{keyword}%'))
        
        # 排序
        if sort_by in allowed_fields:
            col = allowed_fields[sort_by]
            query = query.order_by(col.desc() if order == 'desc' else col.asc())
        
        # 预加载作者信息
        query = query.join(MyUser, Posts.user == MyUser.objectId)
        
        total = query.count()
        posts = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': [post.to_dict(include_author=True, user_id=user_id, sync_like_count=True, sync_reply_count=True) for post in posts],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_post(post_id):
    """获取单个帖子详情"""
    try:
        user_id = request.args.get('user_id')  # 当前查看用户的ID
        
        post = Posts.query.get_or_404(post_id)
        
        # 检查可见性
        if not post.is_visible_to_user(user_id):
            return jsonify({
                'success': False,
                'error': 'Post not visible or not approved'
            }), 403
        
        return jsonify({
            'success': True,
            'data': post.to_dict(include_author=True, user_id=user_id, sync_like_count=True, sync_reply_count=True)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_user_posts(user_id):
    """获取指定用户的帖子列表"""
    try:
        # 验证用户是否存在
        user = MyUser.query.get_or_404(user_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        query = Posts.query.filter_by(user=user_id)
        
        # 如果不是本人查看，只显示公开且已审核的帖子
        if viewer_id != user_id:
            query = query.filter(
                Posts.visible == True,
                Posts.audit_state == 'approved'
            )
        
        # 按创建时间倒序排列
        query = query.order_by(desc(Posts.createdAt))
        
        total = query.count()
        posts = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'posts': [post.to_dict(include_author=False, user_id=viewer_id, sync_like_count=True, sync_reply_count=True) for post in posts],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_posts_by_audit_state(audit_state):
    """根据审核状态获取帖子列表（管理员功能）"""
    try:
        # 验证审核状态
        valid_states = Posts.get_audit_states()
        if audit_state not in valid_states:
            return jsonify({
                'success': False,
                'error': f'Invalid audit state. Valid states: {list(valid_states.keys())}'
            }), 400
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        query = Posts.query.filter_by(audit_state=audit_state)
        query = query.order_by(desc(Posts.createdAt))
        query = query.join(MyUser, Posts.user == MyUser.objectId)
        
        total = query.count()
        posts = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': {
                'audit_state': audit_state,
                'audit_state_name': valid_states[audit_state],
                'posts': [post.to_dict(include_author=True, sync_like_count=True, sync_reply_count=True) for post in posts],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
