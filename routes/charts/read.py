from flask import request, jsonify
from models import Charts

def get_charts():
    """获取所有图表"""
    try:
        # 支持查询参数
        user = request.args.get('user')
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        # 排序参数
        sort_by = request.args.get('sort_by')
        order = (request.args.get('order') or 'desc').lower()
        allowed_fields = {
            'objectId': Charts.objectId,
            'title': Charts.title,
            'achievement': Charts.achievement,
            'user': Charts.user,
            'createdAt': Charts.createdAt,
            'updatedAt': Charts.updatedAt,
        }
        
        query = Charts.query
        
        if user:
            query = query.filter_by(user=user)
        
        # 排序
        if sort_by in allowed_fields:
            col = allowed_fields[sort_by]
            query = query.order_by(col.desc() if order == 'desc' else col.asc())
        else:
            # 默认按创建时间倒序
            query = query.order_by(Charts.createdAt.desc())
        
        # 分页
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        total = query.count()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': [chart.to_dict(include_user=True) for chart in items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_chart(object_id):
    """根据 objectId 获取单个图表"""
    try:
        chart = Charts.query.get_or_404(object_id)
        
        return jsonify({
            'success': True,
            'data': chart.to_dict(include_user=True)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

def get_leaderboard():
    """获取排行榜（按成绩值升序排序，支持分页）
    查询参数：
    - title (可选)：筛选特定标题的排行榜
    - page (可选，默认1)：页码
    - per_page (可选，默认10)：每页数量
    """
    try:
        # 获取查询参数
        title = request.args.get('title')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 10, 1), 100)

        query = Charts.query
        
        # 如果提供了 title 参数，则过滤特定标题
        if title:
            query = query.filter_by(title=title)
            
        query = query.order_by(Charts.achievement.asc())
        total = query.count()
        charts = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1

        return jsonify({
            'success': True,
            'data': [chart.to_dict(include_user=True) for chart in charts],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_rank_by_title_achievement():
    """根据 title 和 achievement 查询排名
    查询参数：
    - title (必填)
    - achievement (必填，float)
    - scope (可选，global|title，默认 global)
    规则：按 achievement 升序，排名为（比该分数低的数量 + 1）。同分并列。
    """
    try:
        title = (request.args.get('title') or '').strip()
        achievement_str = (request.args.get('achievement') or '').strip()
        scope = (request.args.get('scope') or 'global').lower()

        if not title:
            return jsonify({'success': False, 'error': 'title is required'}), 400
        if not achievement_str:
            return jsonify({'success': False, 'error': 'achievement is required'}), 400
        try:
            achievement = float(achievement_str)
        except ValueError:
            return jsonify({'success': False, 'error': 'achievement must be a number'}), 400

        base_query = Charts.query
        if scope == 'title':
            base_query = base_query.filter_by(title=title)

        total = base_query.count()
        lower_count = base_query.filter(Charts.achievement < achievement).count()
        ties_count = base_query.filter(Charts.achievement == achievement).count()
        rank = lower_count + 1

        # 可选：查找是否存在匹配 title 与 achievement 的记录（可能有多条）
        sample = base_query.filter(Charts.title == title, Charts.achievement == achievement).first()
        sample_data = sample.to_dict(include_user=True) if sample else None

        return jsonify({
            'success': True,
            'data': {
                'title': title,
                'achievement': achievement,
                'scope': scope,
                'rank': rank,
                'lower_count': lower_count,
                'ties_count': ties_count,
                'total': total,
                'sample': sample_data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_user_rank_by_title():
    """根据用户ID和title查询用户成绩和排名
    查询参数：
    - user (必填)：用户ID
    - title (必填)：标题
    规则：按 achievement 升序，排名为（比该用户分数低的数量 + 1）。
    """
    try:
        user_id = (request.args.get('user') or '').strip()
        title = (request.args.get('title') or '').strip()

        if not user_id:
            return jsonify({'success': False, 'error': 'user is required'}), 400
        if not title:
            return jsonify({'success': False, 'error': 'title is required'}), 400

        # 查询用户在指定title下的成绩记录
        user_chart = Charts.query.filter_by(user=user_id, title=title).first()
        
        if not user_chart:
            return jsonify({'success': False, 'error': 'No record found for this user and title'}), 404

        # 获取用户的成绩
        user_achievement = user_chart.achievement
        
        # 计算排名：比该用户分数更低的记录数量 + 1
        base_query = Charts.query.filter_by(title=title)
        total_records = base_query.count()
        lower_count = base_query.filter(Charts.achievement < user_achievement).count()
        ties_count = base_query.filter(Charts.achievement == user_achievement).count()
        rank = lower_count + 1

        # 获取用户完整信息的记录
        user_chart_data = user_chart.to_dict(include_user=True)

        return jsonify({
            'success': True,
            'data': {
                'user_info': user_chart_data['user'],
                'achievement': user_achievement,
                'rank': rank,
                'title': title,
                'total_records': total_records,
                'ties_count': ties_count,
                'record': user_chart_data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 