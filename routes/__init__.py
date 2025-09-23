# 导入重构后的蓝图
from .user import user_bp
from .charts import charts_bp
from .image import image_bp
from .history import history_bp
from .releases import releases_bp
from .relationship import relationship_bp
from .posts import posts_bp
from .replies import replies_bp
from .banners import banners_bp
from .likes import likes_bp

# 导出所有蓝图
__all__ = ['user_bp', 'charts_bp', 'image_bp', 'history_bp', 'releases_bp', 'relationship_bp', 'posts_bp', 'replies_bp', 'banners_bp', 'likes_bp']