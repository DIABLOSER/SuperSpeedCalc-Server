from flask import request, jsonify
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
            'data': [post.to_dict() for post in posts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': posts.total,
                'pages': posts.pages
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_forum_post(object_id):
    """根据 objectId 获取单个社区帖子"""
    try:
        post = Forum.query.get_or_404(object_id)
        
        # 增加浏览次数
        post.viewCount += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': post.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

def get_categories():
    """获取所有帖子分类"""
    try:
        # 获取所有不为空的分类
        categories = db.session.query(Forum.category).filter(Forum.category.isnot(None)).distinct().all()
        categories = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({
            'success': True,
            'data': categories
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_popular_posts():
    """获取热门帖子（按浏览次数或点赞数排序）"""
    try:
        limit = request.args.get('limit', 10, type=int)
        sort_by = request.args.get('sort_by', 'viewCount')  # viewCount 或 likeCount
        
        if sort_by == 'likeCount':
            posts = Forum.query.order_by(Forum.likeCount.desc()).limit(limit).all()
        else:
            posts = Forum.query.order_by(Forum.viewCount.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [post.to_dict() for post in posts]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_public_posts():
    """获取所有公开的社区帖子"""
    try:
        limit = request.args.get('limit', 20, type=int)
        posts = Forum.query.filter_by(public=True).order_by(Forum.createdAt.desc()).limit(limit).all()
        return jsonify({
            'success': True,
            'data': [post.to_dict() for post in posts]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 