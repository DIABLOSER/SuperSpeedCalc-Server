from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # 注册蓝图 - 使用新的模块化结构
    from routes import user_bp, charts_bp, forum_bp, image_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(charts_bp, url_prefix='/api/charts')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(image_bp, url_prefix='/api/images')
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'SuperSpeedCalc Server is running'
        })
    
    return app

def init_db(app):
    """初始化数据库"""
    with app.app_context():
        # 导入所有模型以确保它们被注册
        from models import MyUser, Charts, Forum, Image
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    app = create_app('development')
    
    # 创建数据库表
    init_db(app)
    
    # 启动应用
    app.run(host='0.0.0.0', port=5000, debug=True) 