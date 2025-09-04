from .base import db, BaseModel

class UserRelationship(BaseModel):
    """用户关系表 - 存储用户关注关系"""
    __tablename__ = 'user_relationships'
    
    # 关注者的用户ID（谁在关注）
    follower = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 被关注者的用户ID（被关注的人）
    followed = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 建立关联关系
    follower_user = db.relationship('MyUser', foreign_keys=[follower], backref='following_relationships')
    followed_user = db.relationship('MyUser', foreign_keys=[followed], backref='follower_relationships')
    
    # 添加唯一约束，防止重复关注
    __table_args__ = (
        db.UniqueConstraint('follower', 'followed', name='unique_follow_relationship'),
    )
    
    def to_dict(self):
        """重写to_dict方法，包含关联用户信息"""
        result = super().to_dict()
        # 如果需要，可以包含关联用户的基本信息
        if hasattr(self, 'follower_user') and self.follower_user:
            result['follower_info'] = {
                'objectId': self.follower_user.objectId,
                'username': self.follower_user.username,
                'avatar': self.follower_user.avatar
            }
        if hasattr(self, 'followed_user') and self.followed_user:
            result['followed_info'] = {
                'objectId': self.followed_user.objectId,
                'username': self.followed_user.username,
                'avatar': self.followed_user.avatar
            }
        return result
    
    def __repr__(self):
        return f'<UserRelationship follower={self.follower} followed={self.followed}>'
