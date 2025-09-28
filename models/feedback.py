from .base import db, BaseModel
import json

class Feedback(BaseModel):
    """意见反馈表 - 存储用户反馈信息"""
    __tablename__ = 'feedback'
    
    # 反馈用户ID，外键关联到用户表，可为空（允许匿名反馈）
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'))
    
    # 反馈类型，字符串类型，不可为空
    # 可选值：'bug'（Bug报告）, 'feature'（功能建议）, 'complaint'（投诉）, 'praise'（表扬）, 'other'（其他）
    feedback_type = db.Column(db.String(20), nullable=False)
    
    # 反馈标题，最大200字符，不可为空
    title = db.Column(db.String(200), nullable=False)
    
    # 反馈内容，文本类型，不可为空
    content = db.Column(db.Text, nullable=False)
    
    # 反馈状态，字符串类型，默认'pending'（待处理）
    # 可选值：'pending'（待处理）, 'processing'（处理中）, 'resolved'（已解决）, 'closed'（已关闭）
    status = db.Column(db.String(20), default='pending', nullable=False)
    
    # 优先级，字符串类型，默认'medium'（中等）
    # 可选值：'low'（低）, 'medium'（中）, 'high'（高）, 'urgent'（紧急）
    priority = db.Column(db.String(20), default='medium', nullable=False)
    
    # 联系方式，最大100字符，可为空
    contact = db.Column(db.String(100))
    
    # 设备信息，存储为JSON字符串，可为空
    device_info = db.Column(db.Text)
    
    # 应用版本，最大50字符，可为空
    app_version = db.Column(db.String(50))
    
    # 操作系统信息，最大100字符，可为空
    os_info = db.Column(db.String(100))
    
    # 附件列表，存储为JSON字符串，默认为空数组
    attachments = db.Column(db.Text, default='[]')
    
    # 管理员回复，文本类型，可为空
    admin_reply = db.Column(db.Text)
    
    # 管理员回复时间，可为空
    admin_reply_at = db.Column(db.DateTime)
    
    # 处理管理员ID，外键关联到用户表，可为空
    admin_user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'))
    
    # 评分，整数类型，1-5分，可为空
    rating = db.Column(db.Integer)
    
    # 是否公开，布尔类型，默认False（不公开）
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    
    # 标签列表，存储为JSON字符串，默认为空数组
    tags = db.Column(db.Text, default='[]')
    
    def get_device_info_dict(self):
        """获取设备信息（解析JSON）"""
        try:
            if self.device_info:
                return json.loads(self.device_info)
            return {}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def set_device_info_dict(self, device_dict):
        """设置设备信息（转换为JSON）"""
        try:
            if isinstance(device_dict, dict):
                self.device_info = json.dumps(device_dict)
            else:
                self.device_info = None
        except (TypeError, ValueError):
            self.device_info = None
    
    def get_attachments_list(self):
        """获取附件列表（解析JSON）"""
        try:
            if self.attachments:
                return json.loads(self.attachments)
            return []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_attachments_list(self, attachments_list):
        """设置附件列表（转换为JSON）"""
        try:
            if isinstance(attachments_list, list):
                self.attachments = json.dumps(attachments_list)
            else:
                self.attachments = '[]'
        except (TypeError, ValueError):
            self.attachments = '[]'
    
    def add_attachment(self, attachment_url):
        """添加单个附件到列表"""
        attachments_list = self.get_attachments_list()
        if attachment_url and attachment_url not in attachments_list:
            attachments_list.append(attachment_url)
            self.set_attachments_list(attachments_list)
    
    def remove_attachment(self, attachment_url):
        """从列表中移除附件"""
        attachments_list = self.get_attachments_list()
        if attachment_url in attachments_list:
            attachments_list.remove(attachment_url)
            self.set_attachments_list(attachments_list)
    
    def get_tags_list(self):
        """获取标签列表（解析JSON）"""
        try:
            if self.tags:
                return json.loads(self.tags)
            return []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_tags_list(self, tags_list):
        """设置标签列表（转换为JSON）"""
        try:
            if isinstance(tags_list, list):
                self.tags = json.dumps(tags_list)
            else:
                self.tags = '[]'
        except (TypeError, ValueError):
            self.tags = '[]'
    
    def add_tag(self, tag):
        """添加单个标签到列表"""
        tags_list = self.get_tags_list()
        if tag and tag not in tags_list:
            tags_list.append(tag)
            self.set_tags_list(tags_list)
    
    def remove_tag(self, tag):
        """从列表中移除标签"""
        tags_list = self.get_tags_list()
        if tag in tags_list:
            tags_list.remove(tag)
            self.set_tags_list(tags_list)
    
    def is_resolved(self):
        """检查反馈是否已解决"""
        return self.status in ['resolved', 'closed']
    
    def is_high_priority(self):
        """检查是否为高优先级"""
        return self.priority in ['high', 'urgent']
    
    def can_be_edited_by_user(self, user_id):
        """检查用户是否可以编辑此反馈"""
        # 只有反馈作者可以编辑，且状态为待处理或处理中
        return (self.user == user_id and 
                self.status in ['pending', 'processing'])
    
    def can_be_viewed_by_user(self, user_id, is_admin=False):
        """检查用户是否可以查看此反馈"""
        # 管理员可以查看所有反馈
        if is_admin:
            return True
        
        # 反馈作者可以查看自己的反馈
        if self.user == user_id:
            return True
        
        # 公开的反馈所有人都可以查看
        if self.is_public:
            return True
        
        return False
    
    def set_admin_reply(self, reply_content, admin_user_id):
        """设置管理员回复"""
        self.admin_reply = reply_content
        self.admin_user = admin_user_id
        self.admin_reply_at = db.func.now()
        # 如果有回复，状态自动变为已解决
        if self.status == 'pending':
            self.status = 'resolved'
    
    def update_status(self, new_status, admin_user_id=None):
        """更新反馈状态"""
        valid_statuses = ['pending', 'processing', 'resolved', 'closed']
        if new_status in valid_statuses:
            self.status = new_status
            if admin_user_id:
                self.admin_user = admin_user_id
    
    def update_priority(self, new_priority):
        """更新反馈优先级"""
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if new_priority in valid_priorities:
            self.priority = new_priority
    
    def to_dict(self, include_user=True, include_admin=True, user_id=None, is_admin=False):
        """转换为字典，可选择是否包含用户信息"""
        result = super().to_dict()
        
        # 解析JSON字段
        result['device_info'] = self.get_device_info_dict()
        result['attachments'] = self.get_attachments_list()
        result['tags'] = self.get_tags_list()
        
        # 包含用户信息
        if include_user and hasattr(self, 'user_ref') and self.user_ref:
            user_data = {
                'objectId': self.user_ref.objectId,
                'username': self.user_ref.username,
                'avatar': self.user_ref.avatar,
                'admin': self.user_ref.admin
            }
            result['user'] = user_data
        
        # 包含处理管理员信息
        if include_admin and hasattr(self, 'admin_user_ref') and self.admin_user_ref:
            admin_data = {
                'objectId': self.admin_user_ref.objectId,
                'username': self.admin_user_ref.username,
                'avatar': self.admin_user_ref.avatar,
                'admin': self.admin_user_ref.admin
            }
            result['admin_user'] = admin_data
        
        # 添加权限检查结果
        if user_id:
            result['can_edit'] = self.can_be_edited_by_user(user_id)
            result['can_view'] = self.can_be_viewed_by_user(user_id, is_admin)
        else:
            result['can_edit'] = False
            result['can_view'] = self.is_public
        
        # 添加状态信息
        result['is_resolved'] = self.is_resolved()
        result['is_high_priority'] = self.is_high_priority()
        
        return result
    
    @staticmethod
    def get_feedback_types():
        """获取所有可能的反馈类型"""
        return {
            'bug': 'Bug报告',
            'feature': '功能建议',
            'complaint': '投诉',
            'praise': '表扬',
            'other': '其他'
        }
    
    @staticmethod
    def get_statuses():
        """获取所有可能的状态"""
        return {
            'pending': '待处理',
            'processing': '处理中',
            'resolved': '已解决',
            'closed': '已关闭'
        }
    
    @staticmethod
    def get_priorities():
        """获取所有可能的优先级"""
        return {
            'low': '低',
            'medium': '中',
            'high': '高',
            'urgent': '紧急'
        }
    
    @staticmethod
    def get_feedback_stats():
        """获取反馈统计信息"""
        stats = {}
        
        # 按状态统计
        for status, _ in Feedback.get_statuses().items():
            count = Feedback.query.filter_by(status=status).count()
            stats[f'{status}_count'] = count
        
        # 按类型统计
        for feedback_type, _ in Feedback.get_feedback_types().items():
            count = Feedback.query.filter_by(feedback_type=feedback_type).count()
            stats[f'{feedback_type}_count'] = count
        
        # 按优先级统计
        for priority, _ in Feedback.get_priorities().items():
            count = Feedback.query.filter_by(priority=priority).count()
            stats[f'{priority}_priority_count'] = count
        
        # 总体统计
        stats['total_count'] = Feedback.query.count()
        stats['resolved_count'] = Feedback.query.filter(
            Feedback.status.in_(['resolved', 'closed'])
        ).count()
        stats['pending_count'] = Feedback.query.filter_by(status='pending').count()
        
        return stats
    
    def __repr__(self):
        return f'<Feedback {self.objectId} - {self.title}>'