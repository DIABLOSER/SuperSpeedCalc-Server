#!/usr/bin/env python3
"""
数据库迁移脚本：添加history表
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, History

def migrate_add_history_table():
    """添加history表的迁移"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 开始迁移：添加history表...")
            
            # 检查history表是否已存在
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'history' in existing_tables:
                print("✅ history表已存在，跳过创建")
                return
            
            # 创建history表
            History.__table__.create(db.engine)
            print("✅ history表创建成功!")
            
            print("🎉 迁移完成!")
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_add_history_table()
