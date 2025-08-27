#!/usr/bin/env python3
"""
数据库迁移脚本：将my_user表中的experence字段重命名为experience
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from models import db

def migrate_rename_experence_to_experience():
    """将my_user表中的experence字段重命名为experience"""
    app = create_app()
    with app.app_context():
        try:
            print("🔄 开始迁移：将my_user表中的experence字段重命名为experience...")
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            if 'my_user' not in existing_tables:
                print("❌ my_user表不存在，跳过迁移")
                return
            
            columns = [col['name'] for col in inspector.get_columns('my_user')]
            if 'experence' in columns and 'experience' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE my_user RENAME COLUMN experence TO experience"))
                    conn.commit()
                print("✅ 字段重命名成功: experence -> experience")
            elif 'experience' in columns:
                print("✅ experience字段已存在，跳过重命名")
            else:
                print("❌ experence字段不存在，无法重命名")
                return
            
            print("🎉 迁移完成!")
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_rename_experence_to_experience()
