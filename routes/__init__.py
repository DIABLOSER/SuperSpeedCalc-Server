# 导入重构后的蓝图
from .user import user_bp
from .charts import charts_bp
from .forum import forum_bp
from .image import image_bp
from .history import history_bp

# 导出所有蓝图
__all__ = ['user_bp', 'charts_bp', 'forum_bp', 'image_bp', 'history_bp'] 