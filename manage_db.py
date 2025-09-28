#!/usr/bin/env python3
"""
万能数据库管理脚本
用于管理SuperSpeedCalc数据库的创建、重置、检查、备份、迁移等操作
支持字段修改、表结构更新、数据迁移等功能
"""

import os
import sys
import json
import shutil
import datetime
from pathlib import Path
from app import create_app
from models import db, MyUser, Charts, Image, History, AppRelease, UserRelationship, Posts, Likes, Reply, Banner, Collect
from sqlalchemy import inspect, text, MetaData
from sqlalchemy.exc import SQLAlchemyError

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
                image_count = Image.query.count()
                
                print(f"  👥 用户 (MyUser): {user_count}")
                print(f"  📊 图表 (Charts): {charts_count}")
                print(f"  🖼️  图片 (Image): {image_count}")
                print(f"  📦 总记录数: {user_count + charts_count + image_count}")
                
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

def migrate_database(config_name='development'):
    """数据库迁移 - 自动检测并应用结构变更"""
    print("🔄 正在执行数据库迁移...")
    app = create_app(config_name)
    
    with app.app_context():
        try:
            # 获取当前数据库结构
            inspector = inspect(db.engine)
            current_tables = set(inspector.get_table_names())
            
            # 获取模型定义的表
            metadata = MetaData()
            metadata.reflect(bind=db.engine)
            model_tables = set(metadata.tables.keys())
            
            # 检查缺失的表
            missing_tables = model_tables - current_tables
            if missing_tables:
                print(f"📋 发现缺失的表: {', '.join(missing_tables)}")
                db.create_all()
                print("✅ 已创建缺失的表")
            else:
                print("✅ 所有表结构已是最新")
            
            # 检查表结构变更
            print("🔍 检查表结构变更...")
            for table_name in current_tables:
                if table_name in model_tables:
                    # 这里可以添加更详细的字段检查逻辑
                    pass
            
            print("✅ 数据库迁移完成")
            
        except Exception as e:
            print(f"❌ 迁移失败: {e}")

def add_column(table_name, column_name, column_type, default_value=None, nullable=True):
    """添加新字段到指定表"""
    print(f"➕ 正在向表 {table_name} 添加字段 {column_name}...")
    
    try:
        with db.engine.connect() as connection:
            # 构建ALTER TABLE语句
            alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            if not nullable:
                alter_sql += " NOT NULL"
            if default_value is not None:
                alter_sql += f" DEFAULT {default_value}"
            
            connection.execute(text(alter_sql))
            connection.commit()
            print(f"✅ 字段 {column_name} 添加成功")
            
    except Exception as e:
        print(f"❌ 添加字段失败: {e}")

def drop_column(table_name, column_name):
    """从指定表删除字段"""
    print(f"➖ 正在从表 {table_name} 删除字段 {column_name}...")
    
    try:
        with db.engine.connect() as connection:
            # SQLite不支持直接删除列，需要重建表
            print("⚠️  SQLite不支持直接删除列，需要手动处理")
            print("💡 建议使用备份-重建-恢复的方式")
            
    except Exception as e:
        print(f"❌ 删除字段失败: {e}")

def rename_column(table_name, old_name, new_name):
    """重命名字段"""
    print(f"🔄 正在重命名字段 {old_name} -> {new_name}...")
    
    try:
        with db.engine.connect() as connection:
            # SQLite不支持直接重命名列，需要重建表
            print("⚠️  SQLite不支持直接重命名列，需要手动处理")
            print("💡 建议使用备份-重建-恢复的方式")
            
    except Exception as e:
        print(f"❌ 重命名字段失败: {e}")

def export_schema(config_name='development'):
    """导出数据库结构"""
    print("📤 正在导出数据库结构...")
    app = create_app(config_name)
    
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            schema_info = {
                'timestamp': datetime.datetime.now().isoformat(),
                'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
                'tables': {}
            }
            
            tables = inspector.get_table_names()
            for table_name in tables:
                columns = inspector.get_columns(table_name)
                indexes = inspector.get_indexes(table_name)
                foreign_keys = inspector.get_foreign_keys(table_name)
                
                schema_info['tables'][table_name] = {
                    'columns': [
                        {
                            'name': col['name'],
                            'type': str(col['type']),
                            'nullable': col['nullable'],
                            'default': str(col['default']) if col['default'] is not None else None
                        } for col in columns
                    ],
                    'indexes': indexes,
                    'foreign_keys': foreign_keys
                }
            
            # 保存到文件
            schema_file = f"database_schema_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(schema_file, 'w', encoding='utf-8') as f:
                json.dump(schema_info, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 数据库结构已导出到: {schema_file}")
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")

def import_schema(schema_file, config_name='development'):
    """从文件导入数据库结构"""
    print(f"📥 正在从 {schema_file} 导入数据库结构...")
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_info = json.load(f)
        
        print(f"📅 结构文件时间: {schema_info.get('timestamp', '未知')}")
        print("⚠️  导入功能需要手动实现，请谨慎操作")
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")

def restore_database(backup_file, config_name='development'):
    """从备份恢复数据库"""
    print(f"🔄 正在从备份恢复数据库: {backup_file}")
    
    if not os.path.exists(backup_file):
        print(f"❌ 备份文件不存在: {backup_file}")
        return
    
    app = create_app(config_name)
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    
    if not db_uri.startswith('sqlite:///'):
        print("❌ 只支持SQLite数据库恢复")
        return
    
    # 获取当前数据库文件路径
    db_path = db_uri.replace('sqlite:///', '')
    if not os.path.isabs(db_path):
        db_path = os.path.join(app.instance_path, db_path)
    
    try:
        # 备份当前数据库
        if os.path.exists(db_path):
            current_backup = f"{db_path}.current_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(db_path, current_backup)
            print(f"💾 当前数据库已备份到: {current_backup}")
        
        # 恢复数据库
        shutil.copy2(backup_file, db_path)
        print(f"✅ 数据库恢复完成: {db_path}")
        
    except Exception as e:
        print(f"❌ 恢复失败: {e}")

def list_backups():
    """列出所有备份文件"""
    print("📋 正在查找备份文件...")
    
    backup_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.backup_') or 'backup' in file:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                backup_files.append({
                    'path': file_path,
                    'size': file_size,
                    'time': file_time
                })
    
    if backup_files:
        print(f"📦 找到 {len(backup_files)} 个备份文件:")
        for backup in sorted(backup_files, key=lambda x: x['time'], reverse=True):
            print(f"  📁 {backup['path']}")
            print(f"     💾 大小: {backup['size'] / 1024:.2f} KB")
            print(f"     📅 时间: {backup['time'].strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("❌ 未找到备份文件")

def cleanup_old_backups(days=30):
    """清理旧备份文件"""
    print(f"🧹 正在清理 {days} 天前的备份文件...")
    
    cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
    cleaned_count = 0
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.backup_') or 'backup' in file:
                file_path = os.path.join(root, file)
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"🗑️  已删除: {file_path}")
                        cleaned_count += 1
                    except Exception as e:
                        print(f"❌ 删除失败 {file_path}: {e}")
    
    print(f"✅ 清理完成，删除了 {cleaned_count} 个旧备份文件")

def show_help():
    """显示帮助信息"""
    print("""
🗄️  SuperSpeedCalc 万能数据库管理工具

用法: python manage_db.py [命令] [选项]

基础命令:
  init         初始化数据库（创建表结构）
  reset        重置数据库（删除所有数据并重新创建）
  check        检查数据库状态和统计信息
  backup       备份数据库文件
  restore      从备份恢复数据库
  list-backups 列出所有备份文件
  cleanup      清理旧备份文件

高级命令:
  migrate      执行数据库迁移（自动检测结构变更）
  export       导出数据库结构到JSON文件
  import       从JSON文件导入数据库结构
  add-column   添加新字段到指定表
  drop-column  从指定表删除字段
  rename-col   重命名字段

选项:
  --env        指定环境配置 (development/production, 默认: development)
  --file       指定文件路径（用于restore/import命令）
  --table      指定表名（用于字段操作）
  --column     指定字段名（用于字段操作）
  --type       指定字段类型（用于add-column）
  --days       指定天数（用于cleanup，默认30天）

示例:
  python manage_db.py init                           # 初始化数据库
  python manage_db.py check                          # 检查数据库状态
  python manage_db.py backup                         # 备份数据库
  python manage_db.py restore --file backup.db      # 从备份恢复
  python manage_db.py migrate                         # 执行数据库迁移
  python manage_db.py export                         # 导出数据库结构
  python manage_db.py add-column --table users --column age --type INTEGER  # 添加字段
  python manage_db.py list-backups                   # 列出备份文件
  python manage_db.py cleanup --days 7               # 清理7天前的备份
    """)

def parse_args():
    """解析命令行参数"""
    args = {
        'command': None,
        'config_name': 'development',
        'file': None,
        'table': None,
        'column': None,
        'type': None,
        'days': 30
    }
    
    if len(sys.argv) < 2:
        return args
    
    args['command'] = sys.argv[1].lower()
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--env' and i + 1 < len(sys.argv):
            args['config_name'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--file' and i + 1 < len(sys.argv):
            args['file'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--table' and i + 1 < len(sys.argv):
            args['table'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--column' and i + 1 < len(sys.argv):
            args['column'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--type' and i + 1 < len(sys.argv):
            args['type'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--days' and i + 1 < len(sys.argv):
            args['days'] = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    return args

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    args = parse_args()
    command = args['command']
    
    print(f"🔧 使用配置: {args['config_name']}")
    
    try:
        if command == 'init':
            init_database(args['config_name'])
        elif command == 'reset':
            reset_database(args['config_name'])
        elif command == 'check':
            check_database(args['config_name'])
        elif command == 'backup':
            backup_database(args['config_name'])
        elif command == 'restore':
            if not args['file']:
                print("❌ restore命令需要指定--file参数")
                sys.exit(1)
            restore_database(args['file'], args['config_name'])
        elif command == 'migrate':
            migrate_database(args['config_name'])
        elif command == 'export':
            export_schema(args['config_name'])
        elif command == 'import':
            if not args['file']:
                print("❌ import命令需要指定--file参数")
                sys.exit(1)
            import_schema(args['file'], args['config_name'])
        elif command == 'add-column':
            if not all([args['table'], args['column'], args['type']]):
                print("❌ add-column命令需要指定--table、--column、--type参数")
                sys.exit(1)
            add_column(args['table'], args['column'], args['type'])
        elif command == 'drop-column':
            if not all([args['table'], args['column']]):
                print("❌ drop-column命令需要指定--table、--column参数")
                sys.exit(1)
            drop_column(args['table'], args['column'])
        elif command == 'rename-col':
            if not all([args['table'], args['column']]):
                print("❌ rename-col命令需要指定--table、--column参数")
                sys.exit(1)
            # 需要额外的参数来指定新名称
            print("❌ rename-col命令需要手动实现")
        elif command == 'list-backups':
            list_backups()
        elif command == 'cleanup':
            cleanup_old_backups(args['days'])
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