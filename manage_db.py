#!/usr/bin/env python3
"""
数据库管理脚本
用于管理SuperSpeedCalc数据库的创建、重置和检查
"""

import os
import sys
from app import create_app
from models import db, MyUser, Charts, Forum, Image

def init_database(config_name='development'):
    """初始化数据库"""
    print("🔧 正在初始化数据库...")
    app = create_app(config_name)
    
    with app.app_context():
        # 确保instance目录存在
        os.makedirs(app.instance_path, exist_ok=True)
        
        db.create_all()
        print("✅ 数据库和表创建/验证成功!")
        
        # 显示数据库位置
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            if not os.path.isabs(db_path):
                db_path = os.path.join(app.instance_path, db_path)
            print(f"📁 数据库位置: {db_path}")

def reset_database(config_name='development'):
    """重置数据库（删除所有数据）"""
    print("⚠️  警告: 这将删除所有现有数据!")
    confirm = input("确定要继续吗? (yes/no): ")
    
    if confirm.lower() not in ['yes', 'y']:
        print("❌ 操作已取消")
        return
    
    print("🔄 正在重置数据库...")
    app = create_app(config_name)
    
    with app.app_context():
        db.drop_all()
        print("🗑️  已删除所有表")
        
        db.create_all()
        print("✅ 数据库重置完成!")

def check_database(config_name='development'):
    """检查数据库状态"""
    print("🔍 正在检查数据库状态...")
    app = create_app(config_name)
    
    with app.app_context():
        try:
            # 检查数据库连接 - 兼容新版SQLAlchemy
            from sqlalchemy import text
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ 数据库连接正常")
            
            # 获取表名
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 数据库包含 {len(tables)} 个表: {', '.join(tables)}")
            
            # 统计各表记录数
            print("\n📈 各表记录数:")
            try:
                user_count = MyUser.query.count()
                charts_count = Charts.query.count()
                forum_count = Forum.query.count()
                image_count = Image.query.count()
                
                print(f"  👥 用户 (MyUser): {user_count}")
                print(f"  📊 图表 (Charts): {charts_count}")
                print(f"  💬 论坛 (Forum): {forum_count}")
                print(f"  🖼️  图片 (Image): {image_count}")
                print(f"  📦 总记录数: {user_count + charts_count + forum_count + image_count}")
                
            except Exception as e:
                print(f"⚠️  统计记录数时出错: {e}")
                
            # 显示数据库文件信息
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if db_uri.startswith('sqlite:///'):
                db_path = db_uri.replace('sqlite:///', '')
                if not os.path.isabs(db_path):
                    db_path = os.path.join(app.instance_path, db_path)
                
                if os.path.exists(db_path):
                    file_size = os.path.getsize(db_path)
                    print(f"📁 数据库文件: {db_path}")
                    print(f"💾 文件大小: {file_size / 1024:.2f} KB")
                else:
                    print("❌ 数据库文件不存在")
                    
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")

def backup_database(config_name='development'):
    """备份数据库"""
    print("💾 正在备份数据库...")
    app = create_app(config_name)
    
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if not db_uri.startswith('sqlite:///'):
        print("❌ 只支持SQLite数据库备份")
        return
    
    # 获取数据库文件路径
    db_path = db_uri.replace('sqlite:///', '')
    if not os.path.isabs(db_path):
        db_path = os.path.join(app.instance_path, db_path)
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return
    
    # 创建备份文件名
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{db_path}.backup_{timestamp}"
    
    # 复制文件
    import shutil
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ 数据库备份完成: {backup_path}")
    except Exception as e:
        print(f"❌ 备份失败: {e}")

def show_help():
    """显示帮助信息"""
    print("""
🗄️  SuperSpeedCalc 数据库管理工具

用法: python manage_db.py [命令] [选项]

命令:
  init     初始化数据库（创建表结构）
  reset    重置数据库（删除所有数据并重新创建）
  check    检查数据库状态和统计信息
  backup   备份数据库文件
  help     显示此帮助信息

选项:
  --env    指定环境配置 (development/production, 默认: development)

示例:
  python manage_db.py init                    # 初始化数据库
  python manage_db.py check                   # 检查数据库状态
  python manage_db.py reset                   # 重置数据库
  python manage_db.py backup                  # 备份数据库
  python manage_db.py init --env production   # 在生产环境初始化数据库
    """)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # 检查环境配置
    config_name = 'development'
    if '--env' in sys.argv:
        try:
            env_index = sys.argv.index('--env')
            config_name = sys.argv[env_index + 1]
        except (IndexError, ValueError):
            print("❌ --env 参数需要指定配置名称")
            sys.exit(1)
    
    print(f"🔧 使用配置: {config_name}")
    
    try:
        if command == 'init':
            init_database(config_name)
        elif command == 'reset':
            reset_database(config_name)
        elif command == 'check':
            check_database(config_name)
        elif command == 'backup':
            backup_database(config_name)
        elif command in ['help', '--help', '-h']:
            show_help()
        else:
            print(f"❌ 未知命令: {command}")
            print("💡 使用 'python manage_db.py help' 查看可用命令")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ 操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 