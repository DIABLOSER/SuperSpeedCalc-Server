import os
import logging
from datetime import timedelta

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'  # 默认使用 SQLite，可改为 MySQL
    
    # CORS 配置
    CORS_ORIGINS = ["*"]
    
    # JWT 配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # Bmob 配置
    BMOB_APPLICATION_ID = os.environ.get('BMOB_APPLICATION_ID') or '97fc7a013c292b2c90ca9bddcd639bfb'
    BMOB_REST_API_KEY = os.environ.get('BMOB_REST_API_KEY') or '7cc42e8133868d61ff2a70f415ca0b39'
    BMOB_MASTER_KEY = os.environ.get('BMOB_MASTER_KEY') or '2a2107dc1cc9e847f9d57563635961c8'

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
    # 开发环境数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///instance/app_development.db'
    
    # 详细日志配置
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/app_development.log'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 生产环境数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///instance/app_production.db'
    
    # 生产环境日志配置
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/app_production.log'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 