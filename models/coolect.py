from .base import db, BaseModel

class Collect(BaseModel):
    """收藏表 - 存储用户收藏的帖子信息"""
    __tablename__ = 'collect'
    
    # 用户ID，外键关联到用户表
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 帖子ID，外键关联到帖子表
    post = db.Column(db.String(20), db.ForeignKey('posts.objectId'), nullable=False)
    
    # 添加唯一约束，防止用户重复收藏同一帖子
    __table_args__ = (
        db.UniqueConstraint('user', 'post', name='unique_user_post_collect'),
    )
    
    def to_dict(self, include_full_user=True, include_full_post=True):
        """转换为字典，可选择是否包含完整的用户和帖子信息"""
        result = super().to_dict()
        
        # 包含用户信息
        if include_full_user and hasattr(self, 'user_ref') and self.user_ref:
            user_data = {
                'objectId': self.user_ref.objectId,
                'username': self.user_ref.username,
                'avatar': self.user_ref.avatar,
                'bio': self.user_ref.bio,
                'experience': self.user_ref.experience,
                'boluo': self.user_ref.boluo,
                'isActive': self.user_ref.isActive,
                'admin': self.user_ref.admin,
                'sex': self.user_ref.sex,
                'birthday': self.user_ref.birthday.isoformat() if self.user_ref.birthday else None,
                'createdAt': self.user_ref.createdAt.isoformat(),
                'updatedAt': self.user_ref.updatedAt.isoformat()
            }
            result['user'] = user_data
        # 如果不包含完整用户信息，user字段保持为ID字符串
        
        # 包含帖子信息
        if include_full_post and hasattr(self, 'post_ref') and self.post_ref:
            post_data = {
                'objectId': self.post_ref.objectId,
                'content': self.post_ref.content,
                'visible': self.post_ref.visible,
                'audit_state': self.post_ref.audit_state,
                'images': self.post_ref.get_images_list(),
                'likeCount': self.post_ref.likeCount,
                'replyCount': self.post_ref.replyCount,
                'createdAt': self.post_ref.createdAt.isoformat(),
                'updatedAt': self.post_ref.updatedAt.isoformat()
            }
            result['post'] = post_data
        # 如果不包含完整帖子信息，post字段保持为ID字符串
        
        return result
    
    @staticmethod
    def is_user_collected_post(post_id, user_id):
        """检查用户是否已收藏指定帖子"""
        return Collect.query.filter_by(post=post_id, user=user_id).first() is not None
    
    @staticmethod
    def get_user_collect_count(user_id):
        """获取用户收藏的帖子数量"""
        return Collect.query.filter_by(user=user_id).count()
    
    @staticmethod
    def get_post_collect_count(post_id):
        """获取帖子被收藏的数量"""
        return Collect.query.filter_by(post=post_id).count()
    
    @staticmethod
    def get_user_collected_posts(user_id, limit=None, offset=0):
        """获取用户收藏的帖子列表"""
        query = Collect.query.filter_by(user=user_id)
        query = query.order_by(Collect.createdAt.desc())
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    @staticmethod
    def get_post_collectors(post_id, limit=None, offset=0):
        """获取收藏指定帖子的用户列表"""
        query = Collect.query.filter_by(post=post_id)
        query = query.order_by(Collect.createdAt.desc())
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    def __repr__(self):
        return f'<Collect {self.objectId} - User: {self.user}, Post: {self.post}>'