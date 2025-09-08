from flask import request
from models import db, History, MyUser
from sqlalchemy import desc, func, and_
from datetime import datetime, timedelta
from utils.response import (
    success_response, bad_request_response, not_found_response, 
    internal_error_response, paginated_response
)

def get_histories():
    """获取历史记录列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user = request.args.get('user')
        
        # 构建查询
        query = History.query
        
        # 如果指定了用户ID，则只查询该用户的历史记录
        if user:
            query = query.filter(History.user == user)
        
        # 按创建时间倒序排列
        query = query.order_by(desc(History.createdAt))
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        histories = pagination.items
        
        # 转换为字典列表
        history_list = [history.to_dict(include_user=True) for history in histories]
        
        return paginated_response(
            data=history_list,
            page=page,
            per_page=per_page,
            total=pagination.total,
            message='获取历史记录列表成功'
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取历史记录列表失败",
            error_code="GET_HISTORIES_FAILED",
            details=str(e)
        )

def get_history(object_id):
    """获取单个历史记录"""
    try:
        history = History.query.get(object_id)
        
        if not history:
            return not_found_response(
                message='历史记录不存在',
                error_code='HISTORY_NOT_FOUND'
            )
        
        history_dict = history.to_dict(include_user=True)
        
        return success_response(
            data=history_dict,
            message='获取历史记录成功'
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取历史记录失败",
            error_code="GET_HISTORY_FAILED",
            details=str(e)
        )

def get_histories_count():
    """获取历史记录总数"""
    try:
        user = request.args.get('user')
        
        query = History.query
        
        if user:
            count = query.filter(History.user == user).count()
        else:
            count = query.count()
        
        return success_response(
            data={'count': count},
            message='获取历史记录总数成功'
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取历史记录总数失败",
            error_code="GET_HISTORIES_COUNT_FAILED",
            details=str(e)
        )

def get_score_leaderboard():
    """获取用户score得分排行榜"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        period = request.args.get('period', 'all')  # all, daily, monthly, yearly
        
        # 构建基础查询
        query = db.session.query(
            MyUser.objectId,
            MyUser.username,
            MyUser.avatar,
            MyUser.bio,
            MyUser.experience,
            MyUser.boluo,
            MyUser.isActive,
            MyUser.admin,
            MyUser.sex,
            MyUser.birthday,
            MyUser.createdAt,
            MyUser.updatedAt,
            func.sum(History.score).label('total_score'),
            func.count(History.objectId).label('history_count')
        ).join(History, MyUser.objectId == History.user)
        
        # 根据时间段过滤
        now = datetime.utcnow()
        if period == 'daily':
            # 今日数据
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(History.createdAt >= start_date)
        elif period == 'monthly':
            # 本月数据
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(History.createdAt >= start_date)
        elif period == 'yearly':
            # 今年数据
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(History.createdAt >= start_date)
        # period == 'all' 时不添加时间过滤
        
        # 分组并排序
        query = query.group_by(
            MyUser.objectId, MyUser.username, MyUser.avatar, MyUser.bio,
            MyUser.experience, MyUser.boluo, MyUser.isActive,
            MyUser.admin, MyUser.sex, MyUser.birthday, MyUser.createdAt, MyUser.updatedAt
        ).order_by(desc('total_score'))
        
        # 分页
        offset = (page - 1) * per_page
        total_query = query.subquery()
        
        # 获取总数
        total_count = db.session.query(func.count(total_query.c.objectId)).scalar()
        
        # 获取分页数据
        leaderboard_data = query.offset(offset).limit(per_page).all()
        
        # 转换为字典列表
        leaderboard_list = []
        for i, (user_id, username, avatar, bio, experience, boluo, isActive, admin, sex, birthday, createdAt, updatedAt, total_score, history_count) in enumerate(leaderboard_data, 1):
            rank = offset + i
            leaderboard_list.append({
                'rank': rank,
                'user': {
                    'objectId': user_id,
                    'username': username,
                    'avatar': avatar,
                    'bio': bio,
                    # 用户表已移除score，使用0占位
                    'score': 0,
                    'experience': experience or 0,
                    'boluo': boluo or 0,
                    'isActive': isActive,
                    'admin': admin,
                    'sex': sex or 1,
                    'birthday': birthday.isoformat() if birthday else None,
                    'createdAt': createdAt.isoformat() if createdAt else None,
                    'updatedAt': updatedAt.isoformat() if updatedAt else None
                },
                'total_score': total_score or 0,
                'history_count': history_count or 0
            })
        
        # 计算分页信息
        total_pages = (total_count + per_page - 1) // per_page
        
        return paginated_response(
            data=leaderboard_list,
            page=page,
            per_page=per_page,
            total=total_count,
            message=f'获取{period}排行榜成功'
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取排行榜失败",
            error_code="GET_LEADERBOARD_FAILED",
            details=str(e)
        )

def get_user_score_stats():
    """获取用户score统计信息"""
    try:
        user_id = request.args.get('user')
        if not user_id:
            return bad_request_response(
                message='用户ID不能为空',
                error_code='MISSING_USER_ID'
            )
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(
                message='用户不存在',
                error_code='USER_NOT_FOUND'
            )
        
        now = datetime.utcnow()
        
        # 今日统计
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_stats = db.session.query(
            func.sum(History.score).label('total_score'),
            func.count(History.objectId).label('count')
        ).filter(
            and_(History.user == user_id, History.createdAt >= today_start)
        ).first()
        
        # 本月统计
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_stats = db.session.query(
            func.sum(History.score).label('total_score'),
            func.count(History.objectId).label('count')
        ).filter(
            and_(History.user == user_id, History.createdAt >= month_start)
        ).first()
        
        # 今年统计
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        year_stats = db.session.query(
            func.sum(History.score).label('total_score'),
            func.count(History.objectId).label('count')
        ).filter(
            and_(History.user == user_id, History.createdAt >= year_start)
        ).first()
        
        # 总统计
        total_stats = db.session.query(
            func.sum(History.score).label('total_score'),
            func.count(History.objectId).label('count')
        ).filter(History.user == user_id).first()

        # 计算用户在不同周期的排名
        def compute_rank(start_dt=None):
            # 聚合每个用户的总分（按周期过滤）
            base_query = db.session.query(
                History.user.label('user_id'),
                func.sum(History.score).label('total_score')
            )
            if start_dt is not None:
                base_query = base_query.filter(History.createdAt >= start_dt)
            total_per_user_sq = base_query.group_by(History.user).subquery()

            # 当前用户在该周期内的总分与记录数
            user_agg_query = db.session.query(
                func.sum(History.score).label('total_score'),
                func.count(History.objectId).label('count')
            ).filter(History.user == user_id)
            if start_dt is not None:
                user_agg_query = user_agg_query.filter(History.createdAt >= start_dt)
            user_agg = user_agg_query.first()

            # 若该周期无记录，则不参与排名
            if not user_agg or (user_agg.count or 0) == 0:
                return None

            user_total = user_agg.total_score or 0

            # 比当前用户分数高的用户数量 + 1 即为名次（并列采用竞赛排名法）
            higher_count = db.session.query(func.count()).select_from(total_per_user_sq).filter(
                total_per_user_sq.c.total_score > user_total
            ).scalar() or 0

            return higher_count + 1

        ranks = {
            'today': compute_rank(today_start),
            'month': compute_rank(month_start),
            'year': compute_rank(year_start),
            'total': compute_rank(None)
        }
        
        return success_response(
            data={
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar,
                    'bio': user.bio,
                    # 用户表已移除score，返回0
                    'score': 0,
                    'experience': user.experience,
                    'boluo': user.boluo,
                    'isActive': user.isActive,
                    'admin': user.admin,
                    'sex': user.sex,
                    'birthday': user.birthday.isoformat() if user.birthday else None,
                    'createdAt': user.createdAt.isoformat(),
                    'updatedAt': user.updatedAt.isoformat()
                },
                'stats': {
                    'today': {
                        'total_score': today_stats.total_score or 0,
                        'count': today_stats.count or 0,
                        'rank': ranks['today']
                    },
                    'month': {
                        'total_score': month_stats.total_score or 0,
                        'count': month_stats.count or 0,
                        'rank': ranks['month']
                    },
                    'year': {
                        'total_score': year_stats.total_score or 0,
                        'count': year_stats.count or 0,
                        'rank': ranks['year']
                    },
                    'total': {
                        'total_score': total_stats.total_score or 0,
                        'count': total_stats.count or 0,
                        'rank': ranks['total']
                    }
                }
            },
            message='获取用户score统计成功'
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取用户score统计失败",
            error_code="GET_USER_STATS_FAILED",
            details=str(e)
        )
