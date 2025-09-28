from flask import Blueprint, request, jsonify
from models import db, Feedback, MyUser
from utils.response import success_response, error_response
from sqlalchemy import desc, asc, or_, and_
import json

feedback_read_bp = Blueprint('feedback_read', __name__)

@feedback_read_bp.route('/list', methods=['GET'])
def get_feedback_list():
    """获取反馈列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        feedback_type = request.args.get('feedback_type')
        status = request.args.get('status')
        priority = request.args.get('priority')
        user_id = request.args.get('user_id')
        is_public = request.args.get('is_public')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'createdAt')
        sort_order = request.args.get('sort_order', 'desc')
        
        # 构建查询
        query = Feedback.query
        
        # 过滤条件
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        
        if status:
            query = query.filter(Feedback.status == status)
        
        if priority:
            query = query.filter(Feedback.priority == priority)
        
        if user_id:
            query = query.filter(Feedback.user == user_id)
        
        if is_public is not None:
            query = query.filter(Feedback.is_public == (is_public.lower() == 'true'))
        
        # 搜索功能
        if search:
            search_filter = or_(
                Feedback.title.contains(search),
                Feedback.content.contains(search)
            )
            query = query.filter(search_filter)
        
        # 排序
        if hasattr(Feedback, sort_by):
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Feedback, sort_by)))
            else:
                query = query.order_by(asc(getattr(Feedback, sort_by)))
        else:
            query = query.order_by(desc(Feedback.createdAt))
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 转换为字典
        feedbacks = []
        for feedback in pagination.items:
            # 检查用户是否有权限查看此反馈
            if feedback.can_be_viewed_by_user(current_user_id, is_admin):
                feedbacks.append(feedback.to_dict(
                    include_user=True, 
                    include_admin=True,
                    user_id=current_user_id,
                    is_admin=is_admin
                ))
        
        return success_response({
            'feedbacks': feedbacks,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next
            }
        })
        
    except Exception as e:
        return error_response(f'获取反馈列表失败: {str(e)}', 500)

@feedback_read_bp.route('/<feedback_id>', methods=['GET'])
def get_feedback_detail(feedback_id):
    """获取反馈详情"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查用户是否有权限查看此反馈
        if not feedback.can_be_viewed_by_user(current_user_id, is_admin):
            return error_response('没有权限查看此反馈', 403)
        
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'feedback': feedback_data
        })
        
    except Exception as e:
        return error_response(f'获取反馈详情失败: {str(e)}', 500)

@feedback_read_bp.route('/stats', methods=['GET'])
def get_feedback_stats():
    """获取反馈统计信息"""
    try:
        stats = Feedback.get_feedback_stats()
        
        # 添加类型、状态、优先级的详细信息
        stats['feedback_types'] = Feedback.get_feedback_types()
        stats['statuses'] = Feedback.get_statuses()
        stats['priorities'] = Feedback.get_priorities()
        
        return success_response({
            'stats': stats
        })
        
    except Exception as e:
        return error_response(f'获取反馈统计失败: {str(e)}', 500)

@feedback_read_bp.route('/my', methods=['GET'])
def get_my_feedback():
    """获取我的反馈"""
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return error_response('缺少用户ID', 400)
        
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        feedback_type = request.args.get('feedback_type')
        status = request.args.get('status')
        sort_by = request.args.get('sort_by', 'createdAt')
        sort_order = request.args.get('sort_order', 'desc')
        
        # 构建查询
        query = Feedback.query.filter(Feedback.user == user_id)
        
        # 过滤条件
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        
        if status:
            query = query.filter(Feedback.status == status)
        
        # 排序
        if hasattr(Feedback, sort_by):
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Feedback, sort_by)))
            else:
                query = query.order_by(asc(getattr(Feedback, sort_by)))
        else:
            query = query.order_by(desc(Feedback.createdAt))
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 转换为字典
        feedbacks = []
        for feedback in pagination.items:
            feedbacks.append(feedback.to_dict(
                include_user=True, 
                include_admin=True,
                user_id=user_id,
                is_admin=False
            ))
        
        return success_response({
            'feedbacks': feedbacks,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next
            }
        })
        
    except Exception as e:
        return error_response(f'获取我的反馈失败: {str(e)}', 500)

@feedback_read_bp.route('/public', methods=['GET'])
def get_public_feedback():
    """获取公开反馈"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        feedback_type = request.args.get('feedback_type')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'createdAt')
        sort_order = request.args.get('sort_order', 'desc')
        
        # 构建查询（只获取公开的反馈）
        query = Feedback.query.filter(Feedback.is_public == True)
        
        # 过滤条件
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        
        # 搜索功能
        if search:
            search_filter = or_(
                Feedback.title.contains(search),
                Feedback.content.contains(search)
            )
            query = query.filter(search_filter)
        
        # 排序
        if hasattr(Feedback, sort_by):
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Feedback, sort_by)))
            else:
                query = query.order_by(asc(getattr(Feedback, sort_by)))
        else:
            query = query.order_by(desc(Feedback.createdAt))
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 转换为字典
        feedbacks = []
        for feedback in pagination.items:
            feedbacks.append(feedback.to_dict(
                include_user=True, 
                include_admin=False,
                user_id=None,
                is_admin=False
            ))
        
        return success_response({
            'feedbacks': feedbacks,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next
            }
        })
        
    except Exception as e:
        return error_response(f'获取公开反馈失败: {str(e)}', 500)
