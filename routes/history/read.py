from flask import request, jsonify
from models import db, History, MyUser
from sqlalchemy import desc, func, and_
from datetime import datetime, timedelta

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
        
        return jsonify({
            'message': '获取历史记录列表成功',
            'data': history_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取历史记录列表失败: {str(e)}'}), 500

def get_history(object_id):
    """获取单个历史记录"""
    try:
        history = History.query.get(object_id)
        
        if not history:
            return jsonify({'error': '历史记录不存在'}), 404
        
        history_dict = history.to_dict(include_user=True)
        
        return jsonify({
            'message': '获取历史记录成功',
            'data': history_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取历史记录失败: {str(e)}'}), 500

def get_histories_count():
    """获取历史记录总数"""
    try:
        user = request.args.get('user')
        
        query = History.query
        
        if user:
            count = query.filter(History.user == user).count()
        else:
            count = query.count()
        
        return jsonify({
            'message': '获取历史记录总数成功',
            'data': {'count': count}
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取历史记录总数失败: {str(e)}'}), 500

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
        
        return jsonify({
            'message': f'获取{period}排行榜成功',
            'data': leaderboard_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'period': period
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取排行榜失败: {str(e)}'}), 500

def get_user_score_stats():
    """获取用户score统计信息"""
    try:
        user_id = request.args.get('user')
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
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
        
        return jsonify({
            'message': '获取用户score统计成功',
            'data': {
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
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户score统计失败: {str(e)}'}), 500
