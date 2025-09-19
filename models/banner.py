from .base import db, BaseModel
import json

class Banner(BaseModel):
    """横幅表 - 存储应用横幅广告和轮播图信息"""
    __tablename__ = 'banners'
    
    # 横幅标题，字符串类型，不可为空
    title = db.Column(db.String(200), nullable=False)
    
    # 是否展示，布尔类型，默认True
    show = db.Column(db.Boolean, default=True, nullable=False)
    
    # 是否可点击，布尔类型，默认True
    click = db.Column(db.Boolean, default=True, nullable=False)
    
    # 横幅内容/描述，文本类型，可为空
    content = db.Column(db.Text, nullable=True)
    
    # 点击动作，web网页user用户post帖子
    action = db.Column(db.String(500), nullable=True)
    
    # 图片链接，字符串类型，存储横幅图片的URL
    imageurl = db.Column(db.String(500), nullable=True)
    
    # 排序权重，数字越小优先级越高，默认0
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    
    def is_active(self):
        """检查横幅是否处于活跃状态"""
        # 只检查show状态
        return self.show
    
    def to_dict(self):
        """转换为字典"""
        result = super().to_dict()
        
        # 添加状态信息
        result['is_active'] = self.is_active()
        
        return result
    
    @staticmethod
    def get_active_banners(limit=None):
        """获取活跃的横幅列表"""
        query = Banner.query.filter(Banner.show == True)
        
        # 按排序权重和创建时间排序
        query = query.order_by(Banner.sort_order.asc(), Banner.createdAt.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_action_types():
        """获取所有动作类型说明"""
        return {
            'url': '跳转到外部链接',
            'page': '跳转到应用内页面',
            'modal': '打开弹窗',
            'download': '下载文件',
            'share': '分享功能',
            'none': '无动作'
        }
    
    def __repr__(self):
        return f'<Banner {self.title}>'
