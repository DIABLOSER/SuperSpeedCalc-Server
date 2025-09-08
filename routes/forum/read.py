from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Forum

def get_forum_posts():
    """获取所有社区帖子"""
    try:
        # 支持查询参数
        category = request.args.get('category')
        user = request.args.get('user')
        isPinned = request.args.get('isPinned')
        public = request.args.get('public')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Forum.query
        
        if category:
            query = query.filter_by(category=category)
        if user:
            query = query.filter_by(user=user)
        if isPinned is not None:
            query = query.filter_by(isPinned=isPinned.lower() == 'true')
        if public is not None:
            query = query.filter_by(public=public.lower() == 'true')
        
        # 排序：置顶帖在前，然后按创建时间倒序
        query = query.order_by(Forum.isPinned.desc(), Forum.createdAt.desc())
        
        # 分页
        posts = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [post.to_dict(include_user=True) for post in posts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': posts.total,
                'pages': posts.pages
            }
        })
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_forum_post(object_id):
    """根据 objectId 获取单个社区帖子"""
    try:
        post = Forum.query.get_or_404(object_id)
        
        # 增加浏览次数
        post.viewCount += 1
        db.session.commit()
        
        return success_response(data=post.to_dict(include_user=True)
        )
    except Exception as e:
        return internal_error_response(message=str(e), code=404)

def get_categories():
    """获取所有帖子分类（支持分页）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 50, 1), 200)

        base_query = db.session.query(Forum.category).filter(Forum.category.isnot(None)).distinct()
        # 排序：按分类名称升序，确保分页稳定
        base_query = base_query.order_by(Forum.category.asc())

        # 统计总数（去重后的分类数）
        total = db.session.query(db.func.count(db.func.distinct(Forum.category))).scalar() or 0
        items = base_query.limit(per_page).offset((page - 1) * per_page).all()
        categories = [cat[0] for cat in items if cat[0]]

        pages = (total + per_page - 1) // per_page if per_page else 1

        return jsonify({
            'success': True,
            'data': categories,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_popular_posts():
    """获取热门帖子（按浏览次数或点赞数排序，支持分页）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 10, 1), 100)

        sort_by = request.args.get('sort_by', 'viewCount')  # viewCount 或 likeCount

        query = Forum.query
        if sort_by == 'likeCount':
            query = query.order_by(Forum.likeCount.desc())
        else:
            query = query.order_by(Forum.viewCount.desc())

        total = query.count()
        posts = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1

        return jsonify({
            'success': True,
            'data': [post.to_dict(include_user=True) for post in posts],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_public_posts():
    """获取所有公开的社区帖子（支持分页）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)

        query = Forum.query.filter_by(public=True).order_by(Forum.createdAt.desc())
        total = query.count()
        posts = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1

        return jsonify({
            'success': True,
            'data': [post.to_dict(include_user=True) for post in posts],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
    except Exception as e:
        return internal_error_response(message=str(e), code=500) 