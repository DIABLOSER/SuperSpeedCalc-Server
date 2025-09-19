from .base import db, BaseModel

class Likes(BaseModel):
    """点赞表 - 存储用户对帖子的点赞关系"""
    __tablename__ = 'likes'
    
    # 帖子ID，外键关联到帖子表
    post = db.Column(db.String(20), db.ForeignKey('posts.objectId'), nullable=False)
    
    # 用户ID，外键关联到用户表
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 建立关联关系 - 使用 'select' 以便获取完整对象信息
    post_ref = db.relationship('Posts', backref='post_likes', lazy='select')
    user_ref = db.relationship('MyUser', backref='user_likes', lazy='select')
    
    # 添加唯一约束，防止同一用户多次点赞同一帖子
    __table_args__ = (
        db.UniqueConstraint('post', 'user', name='unique_post_user_like'),
    )
    
    def to_dict(self, include_details=True, include_full_post=False, include_full_user=True):
        """转换为字典 - 返回完整的关联对象信息"""
        result = super().to_dict()
        
        # 始终包含完整的用户信息
        if include_full_user and self.user_ref:
            result['user_data'] = self.user_ref.to_dict(include_stats=False)
        elif self.user_ref:
            result['user_data'] = {
                'objectId': self.user_ref.objectId,
                'username': self.user_ref.username,
                'avatar': self.user_ref.avatar,
                'bio': self.user_ref.bio
            }
        else:
            result['user_data'] = None
        
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
                'images': self.post_ref.get_images_list(),
                'createdAt': self.post_ref.createdAt.isoformat() if self.post_ref.createdAt else None,
                'user': {
                    'objectId': self.post_ref.user_ref.objectId,
                    'username': self.post_ref.user_ref.username,
                    'avatar': self.post_ref.user_ref.avatar
                } if self.post_ref.user_ref else None
            }
        else:
            result['post_data'] = None
        
        # 移除向后兼容字段
        
        return result
    
    @staticmethod
    def get_post_like_count(post_id):
        """获取指定帖子的点赞数量"""
        return Likes.query.filter_by(post=post_id).count()
    
    @staticmethod
    def is_user_liked_post(post_id, user_id):
        """检查用户是否已点赞指定帖子"""
        if not user_id:
            return False
        return Likes.query.filter_by(post=post_id, user=user_id).first() is not None
    
    @staticmethod
    def get_user_liked_posts(user_id, limit=None):
        """获取用户点赞的帖子列表"""
        query = Likes.query.filter_by(user=user_id).order_by(Likes.createdAt.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @staticmethod
    def get_post_likers(post_id, limit=None):
        """获取点赞某帖子的用户列表"""
        query = Likes.query.filter_by(post=post_id).order_by(Likes.createdAt.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def __repr__(self):
        return f'<Likes post={self.post} user={self.user}>'
