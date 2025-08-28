from .base import db, BaseModel

class Forum(BaseModel):
    """社区表 - 存储社区帖子信息"""
    __tablename__ = 'forum'
    
    # 帖子内容，文本类型，不可为空，存储帖子的详细内容
    content = db.Column(db.Text, nullable=False)
    
    # 帖子分类，最大50字符，可为空，用于帖子分类管理（如：公告、讨论、求助等）
    category = db.Column(db.String(50))
    
    # 标签列表，JSON格式，可为空，存储帖子的标签数组，便于搜索和分类
    tags = db.Column(db.JSON)
    
    # 是否公开，布尔类型，默认True，控制帖子是否对所有用户可见
    public = db.Column(db.Boolean, default=True)
    
    # 图片列表，JSON格式，可为空，存储帖子相关图片的URL数组
    images = db.Column(db.JSON)
    
    # 浏览次数，整数类型，默认0，记录帖子被查看的次数
    viewCount = db.Column(db.Integer, default=0)
    
    # 点赞数量，整数类型，默认0，记录用户对帖子的点赞次数
    likeCount = db.Column(db.Integer, default=0)
    
    # 回复数量，整数类型，默认0，记录帖子收到的回复数量
    replyCount = db.Column(db.Integer, default=0)
    
    # 是否置顶，布尔类型，默认False，控制帖子是否在列表顶部显示
    isPinned = db.Column(db.Boolean, default=False)
    
    # 是否关闭，布尔类型，默认False，控制帖子是否禁止回复和互动
    isClosed = db.Column(db.Boolean, default=False)
    
    # 外键：关联用户表的objectId，不可为空，表示帖子的作者
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
        # 如果不包含用户信息，user字段保持为ID字符串
        
        return result
    
    def __repr__(self):
        return f'<Forum {self.objectId}>' 