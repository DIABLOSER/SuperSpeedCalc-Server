from .base import db, BaseModel
import json

class Posts(BaseModel):
    """帖子表 - 存储用户发布的帖子信息"""
    __tablename__ = 'posts'
    
    # 发帖用户ID，外键关联到用户表
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 帖子内容，文本类型，不可为空
    content = db.Column(db.Text, nullable=False)
    
    # 是否公开可见，布尔类型，默认True（公开）
    visible = db.Column(db.Boolean, default=True, nullable=False)
    
    # 审核状态，字符串类型，默认'pending'（待审核）
    # 可选值：'pending'（待审核）, 'approved'（已通过）, 'rejected'（已拒绝）
    audit_state = db.Column(db.String(20), default='pending', nullable=False)
    
    # 图片列表，存储为JSON字符串，默认为空数组
    images = db.Column(db.Text, default='[]')
    
    # 点赞数量，整数类型，默认0
    likeCount = db.Column(db.Integer, default=0, nullable=False)
    
    # 评论数量，整数类型，默认0
    replyCount = db.Column(db.Integer, default=0, nullable=False)
    
    
    def get_images_list(self):
        """获取图片列表（解析JSON）"""
        try:
            if self.images:
                return json.loads(self.images)
            return []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_images_list(self, images_list):
        """设置图片列表（转换为JSON）"""
        try:
            if isinstance(images_list, list):
                self.images = json.dumps(images_list)
            else:
                self.images = '[]'
        except (TypeError, ValueError):
            self.images = '[]'
    
    def add_image(self, image_url):
        """添加单个图片到列表"""
        images_list = self.get_images_list()
        if image_url and image_url not in images_list:
            images_list.append(image_url)
            self.set_images_list(images_list)
    
    def remove_image(self, image_url):
        """从列表中移除图片"""
        images_list = self.get_images_list()
        if image_url in images_list:
            images_list.remove(image_url)
            self.set_images_list(images_list)
    
    def is_approved(self):
        """检查帖子是否已审核通过"""
        return self.audit_state == 'approved'
    
    def is_visible_to_user(self, user_id=None):
        """检查帖子对指定用户是否可见"""
        # 不可见的帖子只有作者可以看到
        if not self.visible:
            return user_id == self.user
        
        # 未审核通过的帖子只有作者可以看到
        if not self.is_approved():
            return user_id == self.user
        
        return True
    
    def get_actual_like_count(self):
        """获取实际点赞数量（基于likes表）"""
        from .likes import Likes
        return Likes.get_post_like_count(self.objectId)
    
    def is_liked_by_user(self, user_id):
        """检查用户是否已点赞此帖子"""
        from .likes import Likes
        return Likes.is_user_liked_post(self.objectId, user_id)
    
    def get_likers(self, limit=None):
        """获取点赞此帖子的用户列表"""
        from .likes import Likes
        return Likes.get_post_likers(self.objectId, limit)
    
    def sync_like_count(self):
        """同步点赞数量（将likes表的实际数量同步到likeCount字段）"""
        actual_count = self.get_actual_like_count()
        if self.likeCount != actual_count:
            self.likeCount = actual_count
            return True  # 表示数据被更新
        return False  # 表示数据未变化
    
    def get_actual_reply_count(self):
        """获取实际评论数量（基于replies表）"""
        from .reply import Reply
        return Reply.get_post_reply_count(self.objectId)
    
    def get_first_level_reply_count(self):
        """获取一级评论数量"""
        from .reply import Reply
        return Reply.get_post_reply_count(self.objectId, level=1)
    
    def get_second_level_reply_count(self):
        """获取二级评论数量"""
        from .reply import Reply
        return Reply.get_post_reply_count(self.objectId, level=2)
    
    def get_replies(self, level=None, limit=None, offset=0):
        """获取帖子的评论列表"""
        from .reply import Reply
        
        query = Reply.query.filter_by(post=self.objectId)
        
        if level == 1:
            # 只获取一级评论
            query = query.filter(Reply.parent.is_(None))
        elif level == 2:
            # 只获取二级评论
            query = query.filter(Reply.parent.isnot(None))
        
        # 按创建时间排序
        query = query.order_by(Reply.createdAt.asc())
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    def sync_reply_count(self):
        """同步评论数量（将replies表的实际数量同步到replyCount字段）"""
        actual_count = self.get_actual_reply_count()
        if self.replyCount != actual_count:
            self.replyCount = actual_count
            return True  # 表示数据被更新
        return False  # 表示数据未变化
    
    def to_dict(self, include_user=True, user_id=None, sync_like_count=False, sync_reply_count=False, include_full_user=True):
        """转换为字典，可选择是否包含用户信息"""
        result = super().to_dict()
        
        # 解析图片列表
        result['images'] = self.get_images_list()
        
        # 同步点赞数量（如果需要）
        if sync_like_count:
            self.sync_like_count()
            result['likeCount'] = self.likeCount
        
        # 同步评论数量（如果需要）
        if sync_reply_count:
            self.sync_reply_count()
            result['replyCount'] = self.replyCount
        
        # 包含用户信息，但不包含敏感字段
        if include_user and hasattr(self, 'user_ref') and self.user_ref:
            if include_full_user:
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
            else:
                user_data = {
                    'objectId': self.user_ref.objectId,
                    'username': self.user_ref.username,
                    'avatar': self.user_ref.avatar,
                    'bio': self.user_ref.bio,
                    'experience': self.user_ref.experience,
                    'admin': self.user_ref.admin
                }
            result['user'] = user_data
        # 如果不包含用户信息，user字段保持为ID字符串
        
        # 添加用户相关的信息
        if user_id:
            result['is_liked_by_user'] = self.is_liked_by_user(user_id)
        else:
            result['is_liked_by_user'] = False
        
        # 添加可见性检查结果
        result['is_visible'] = self.is_visible_to_user(user_id)
        result['is_approved'] = self.is_approved()
        
        # 添加统计信息
        result['stats'] = {
            'likeCount': self.likeCount,
            'replyCount': self.replyCount,
            'actual_like_count': self.get_actual_like_count(),
            'actual_reply_count': self.get_actual_reply_count(),
            'first_level_reply_count': self.get_first_level_reply_count(),
            'second_level_reply_count': self.get_second_level_reply_count()
        }
        
        # 移除向后兼容字段，只保留stats中的统计信息
        
        return result
    
    @staticmethod
    def get_audit_states():
        """获取所有可能的审核状态"""
        return {
            'pending': '待审核',
            'approved': '已通过', 
            'rejected': '已拒绝'
        }
    
    def __repr__(self):
        return f'<Posts {self.objectId} by {self.user}>'
