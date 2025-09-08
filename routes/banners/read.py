from flask import jsonify, request
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Banner
from sqlalchemy import desc, asc, or_, func

def get_banners():
    """获取横幅列表（支持排序、分页、筛选）"""
    try:
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 排序参数
        sort_by = request.args.get('sort_by', 'sort_order')
        order = (request.args.get('order') or 'asc').lower()
        
        # 筛选参数
        show_only = request.args.get('show_only', 'false').lower() == 'true'
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        
        # 搜索关键词
        keyword = (request.args.get('keyword') or '').strip()
        
        # 允许排序的字段
        allowed_fields = {
            'title': Banner.title,
            'sort_order': Banner.sort_order,
            'createdAt': Banner.createdAt,
            'updatedAt': Banner.updatedAt
        }
        
        query = Banner.query
        
        # 只显示启用的
        if show_only or active_only:
            query = query.filter(Banner.show == True)
        
        # 关键词搜索
        if keyword:
            pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    Banner.title.ilike(pattern),
                    Banner.content.ilike(pattern)
                )
            )
        
        # 排序
        if sort_by in allowed_fields:
            col = allowed_fields[sort_by]
            if order == 'desc':
                query = query.order_by(col.desc())
            else:
                query = query.order_by(col.asc())
        else:
            # 默认排序：按sort_order升序，然后按创建时间降序
            query = query.order_by(Banner.sort_order.asc(), Banner.createdAt.desc())
        
        total = query.count()
        banners = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': [banner.to_dict() for banner in banners],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_banner(banner_id):
    """获取单个横幅详情"""
    try:
        banner = Banner.query.get_or_404(banner_id)
        
        return success_response(data=banner.to_dict()
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_active_banners():
    """获取活跃的横幅列表（客户端使用）"""
    try:
        # 筛选参数
        limit = request.args.get('limit', type=int)
        
        # 获取活跃横幅
        banners = Banner.get_active_banners(limit=limit)
        
        return success_response(
            data={
                'banners': [banner.to_dict() for banner in banners],
                'total': len(banners),
                'action_types': Banner.get_action_types()
            }
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_banner_stats():
    """获取横幅基本统计信息（管理员功能）"""
    try:
        # 验证管理员权限
        admin_user_id = request.args.get('admin_user_id')
        if admin_user_id:
            from models import MyUser
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user or not admin_user.admin:
                return internal_error_response(message='Permission denied. Admin access required.'
                , code=403)
        
        # 统计基本数据
        total_banners = Banner.query.count()
        active_banners = len(Banner.get_active_banners())
        visible_banners = Banner.query.filter(Banner.show == True).count()
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_banners': total_banners,
                    'active_banners': active_banners,
                    'visible_banners': visible_banners
                }
            }
        })
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)
