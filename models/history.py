from .base import db, BaseModel

class History(BaseModel):
    """历史记录表 - 存储用户的历史记录信息"""
    __tablename__ = 'history'
    
    # 标题，最大200字符，不可为空，用于描述历史记录的内容
    title = db.Column(db.String(200), nullable=False)
    
    # 分数，整数类型，可以为正数或负数，不可为空，用于记录用户的得分
    score = db.Column(db.Integer, nullable=False)
    
    # 外键：关联用户表的objectId，不可为空，表示历史记录的所有者
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    def to_dict(self, include_user=True):
        """将模型转换为字典，可选择是否包含用户信息"""
        result = super().to_dict()
        
        if include_user and hasattr(self, 'user_ref') and self.user_ref:
            # 包含用户信息，但不包含敏感字段
            user_data = {
                'objectId': self.user_ref.objectId,
                'username': self.user_ref.username,
                'avatar': self.user_ref.avatar,
                'bio': self.user_ref.bio,
                'score': self.user_ref.score,
                'experence': self.user_ref.experence,
                'boluo': self.user_ref.boluo,
                'isActive': self.user_ref.isActive,
                'admin': self.user_ref.admin,
                'sex': self.user_ref.sex,
                'birthday': self.user_ref.birthday.isoformat() if self.user_ref.birthday else None,
                'createdAt': self.user_ref.createdAt.isoformat(),
                'updatedAt': self.user_ref.updatedAt.isoformat()
            }
            result['user'] = user_data
        # 如果不包含用户信息，user字段保持为ID字符串
        
        return result
    
    def __repr__(self):
        return f'<History {self.title}>'
