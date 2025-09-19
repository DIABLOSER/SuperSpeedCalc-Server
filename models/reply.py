from .base import db, BaseModel

class Reply(BaseModel):
    """评论表 - 存储帖子的评论和回复信息"""
    __tablename__ = 'replies'
    
    # 帖子ID，外键关联到帖子表
    post = db.Column(db.String(20), db.ForeignKey('posts.objectId'), nullable=False)
    
    # 评论用户ID，外键关联到用户表
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 接收者用户ID，外键关联到用户表，可为空（一级评论时为空）
    recipient = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=True)
    
    # 评论内容，文本类型，不可为空
    content = db.Column(db.Text, nullable=False)
    
    # 父评论ID，如果为空则为一级评论，不为空则为二级评论
    parent = db.Column(db.String(20), db.ForeignKey('replies.objectId'), nullable=True)
    
    # 建立关联关系 - 使用 'select' 以便获取完整对象信息
    post_ref = db.relationship('Posts', backref='post_replies', lazy='select')
    user_ref = db.relationship('MyUser', foreign_keys=[user], backref='user_replies', lazy='select')
    recipient_ref = db.relationship('MyUser', foreign_keys=[recipient], backref='received_replies', lazy='select')
    
    # 自引用关系：父评论和子评论
    parent_reply = db.relationship('Reply', remote_side='Reply.objectId', backref='child_replies', lazy='select')
    
    def is_first_level(self):
        """检查是否为一级评论"""
        return self.parent is None
    
    def is_second_level(self):
        """检查是否为二级评论"""
        return self.parent is not None
    
    def get_first_level_parent(self):
        """获取一级父评论（如果是二级评论）"""
        if self.is_first_level():
            return self
        return Reply.query.get(self.parent)
    
    def get_reply_count(self):
        """获取此评论的回复数量（只适用于一级评论）"""
        if self.is_second_level():
            return 0
        return Reply.query.filter_by(parent=self.objectId).count()
    
    def get_child_replies(self, limit=None):
        """获取子回复列表（只适用于一级评论）"""
        if self.is_second_level():
            return []
        
        query = Reply.query.filter_by(parent=self.objectId).order_by(Reply.createdAt.asc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def can_be_replied(self):
        """检查是否可以被回复（只有一级评论可以被回复）"""
        return self.is_first_level()
    
    def to_dict(self, include_details=True, include_children=False, include_full_post=False):
        """转换为字典 - 返回完整的关联对象信息"""
        result = super().to_dict()
        
        # 始终包含完整的用户信息
        if self.user_ref:
            result['user_data'] = self.user_ref.to_dict(include_stats=False)
        else:
            result['user_data'] = None
        
        # 包含接收者完整信息（如果有）
        if self.recipient and self.recipient_ref:
            result['recipient_data'] = self.recipient_ref.to_dict(include_stats=False)
        else:
            result['recipient_data'] = None
        
        # 包含帖子信息
        if include_full_post and self.post_ref:
            # 返回完整帖子信息
            result['post_data'] = self.post_ref.to_dict(include_user=True, sync_like_count=False, sync_reply_count=False)
        elif self.post_ref:
            # 返回帖子摘要信息
            result['post_data'] = {
                'objectId': self.post_ref.objectId,
                'content': self.post_ref.content,
                'content_preview': self.post_ref.content[:50] + '...' if len(self.post_ref.content) > 50 else self.post_ref.content,
                'visible': self.post_ref.visible,
                'audit_state': self.post_ref.audit_state,
                'likeCount': self.post_ref.likeCount,
                'replyCount': self.post_ref.replyCount,
                'createdAt': self.post_ref.createdAt.isoformat() if self.post_ref.createdAt else None,
                'user': {
                    'objectId': self.post_ref.user_ref.objectId,
                    'username': self.post_ref.user_ref.username,
                    'avatar': self.post_ref.user_ref.avatar
                } if self.post_ref.user_ref else None
            }
        else:
            result['post_data'] = None
        
        # 包含父评论信息（如果是二级评论）
        if self.is_second_level() and self.parent_reply:
            result['parent_reply_data'] = {
                'objectId': self.parent_reply.objectId,
                'content': self.parent_reply.content,
                'content_preview': self.parent_reply.content[:30] + '...' if len(self.parent_reply.content) > 30 else self.parent_reply.content,
                'user_info': {
                    'objectId': self.parent_reply.user_ref.objectId,
                    'username': self.parent_reply.user_ref.username,
                    'avatar': self.parent_reply.user_ref.avatar
                } if self.parent_reply.user_ref else None,
                'createdAt': self.parent_reply.createdAt.isoformat() if self.parent_reply.createdAt else None
            }
        else:
            result['parent_reply_data'] = None
        
        # 添加评论层级信息
        result['level'] = 1 if self.is_first_level() else 2
        result['is_first_level'] = self.is_first_level()
        result['is_second_level'] = self.is_second_level()
        
        # 如果是一级评论，包含回复统计和子回复
        if self.is_first_level():
            result['reply_count'] = self.get_reply_count()
            
            # 如果需要包含子回复
            if include_children:
                child_replies = self.get_child_replies()
                result['child_replies'] = [
                    child.to_dict(include_details=include_details, include_children=False, include_full_post=False) 
                    for child in child_replies
                ]
            else:
                result['child_replies'] = []
        else:
            result['reply_count'] = 0
            result['child_replies'] = []
        
        # 移除向后兼容字段
        
        return result
    
    @staticmethod
    def get_post_reply_count(post_id, level=None):
        """获取指定帖子的评论数量"""
        query = Reply.query.filter_by(post=post_id)
        
        if level == 1:
            # 只统计一级评论
            query = query.filter(Reply.parent.is_(None))
        elif level == 2:
            # 只统计二级评论
            query = query.filter(Reply.parent.isnot(None))
        # level为None时统计所有评论
        
        return query.count()
    
    @staticmethod
    def get_user_reply_count(user_id):
        """获取用户的评论总数"""
        return Reply.query.filter_by(user=user_id).count()
    
    def __repr__(self):
        level = "L1" if self.is_first_level() else "L2"
        return f'<Reply {level} {self.objectId} by {self.user} on {self.post}>'
