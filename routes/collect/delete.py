from flask import request
from utils.response import (
    success_response, internal_error_response,
    not_found_response, bad_request_response
)
from models import db, Posts, MyUser, Collect

def delete_collect():
    """取消收藏帖子"""
    try:
        data = request.get_json()
        
        post_id = data.get('post_id')
        user_id = data.get('user_id')
        
        if not post_id or not user_id:
            return bad_request_response(message='post_id and user_id are required')
        
        # 验证帖子是否存在
        post = Posts.query.get(post_id)
        if not post:
            return not_found_response(message="帖子不存在")
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 查找收藏记录
        collect_record = Collect.query.filter_by(post=post_id, user=user_id).first()
        if not collect_record:
            return bad_request_response(message='用户未收藏此帖子')
        
        # 删除收藏记录
        db.session.delete(collect_record)
        db.session.commit()
        
        return success_response(
            data={
                'post_id': post.objectId,
                'user_id': user_id,
                'is_collected_by_user': False
            },
            message='取消收藏成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'取消收藏失败: {str(e)}')

def delete_collect_by_id(collect_id):
    """通过收藏ID删除收藏记录"""
    try:
        # 查找收藏记录
        collect_record = Collect.query.get(collect_id)
        if not collect_record:
            return not_found_response(message="收藏记录不存在")
        
        post_id = collect_record.post
        user_id = collect_record.user
        
        # 删除收藏记录
        db.session.delete(collect_record)
        db.session.commit()
        
        return success_response(
            data={
                'collect_id': collect_id,
                'post_id': post_id,
                'user_id': user_id,
                'is_collected_by_user': False
            },
            message='删除收藏记录成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'删除收藏记录失败: {str(e)}')

def clear_user_collects(user_id):
    """清空用户的所有收藏"""
    try:
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 获取用户的所有收藏记录
        collects = Collect.query.filter_by(user=user_id).all()
        collect_count = len(collects)
        
        if collect_count == 0:
            return success_response(
                data={
                    'user_id': user_id,
                    'deleted_count': 0
                },
                message='用户没有收藏记录'
            )
        
        # 删除所有收藏记录
        for collect in collects:
            db.session.delete(collect)
        
        db.session.commit()
        
        return success_response(
            data={
                'user_id': user_id,
                'deleted_count': collect_count
            },
            message=f'成功清空用户收藏，删除了 {collect_count} 条记录'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'清空用户收藏失败: {str(e)}')
