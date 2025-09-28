from utils.response import (
    success_response, internal_error_response,
    not_found_response
)
from models import db, Collect

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
