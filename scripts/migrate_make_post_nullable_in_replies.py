#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：修改replies表的post字段为可空
这样删除帖子时不会影响评论数据，评论可以独立存在
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

app = create_app('development')

def migrate_make_post_nullable():
    """修改replies表的post字段为可空"""
    with app.app_context():
        try:
            print("🔄 开始迁移：修改replies表的post字段为可空...")
            
            # 检查当前约束
            with db.engine.connect() as conn:
                result = conn.execute(db.text("PRAGMA table_info(replies)"))
                columns = result.fetchall()
                
                print("📋 当前replies表结构：")
                for col in columns:
                    print(f"   {col[1]} - {col[2]} - nullable: {not col[3]}")
                
                # 修改post字段为可空
                # SQLite不支持直接修改列约束，需要重建表
                print("\n🔧 重建replies表以支持可空的post字段...")
                
                # 1. 创建新表
                conn.execute(db.text("""
                    CREATE TABLE replies_new (
                        objectId VARCHAR(20) PRIMARY KEY,
                        post VARCHAR(20),
                        user VARCHAR(20) NOT NULL,
                        recipient VARCHAR(20),
                        content TEXT NOT NULL,
                        parent VARCHAR(20),
                        createdAt DATETIME NOT NULL,
                        updatedAt DATETIME NOT NULL,
                        FOREIGN KEY (user) REFERENCES my_user(objectId),
                        FOREIGN KEY (recipient) REFERENCES my_user(objectId),
                        FOREIGN KEY (parent) REFERENCES replies(objectId)
                    )
                """))
                
                # 2. 复制数据
                conn.execute(db.text("""
                    INSERT INTO replies_new 
                    SELECT objectId, post, user, recipient, content, parent, createdAt, updatedAt 
                    FROM replies
                """))
                
                # 3. 删除旧表
                conn.execute(db.text("DROP TABLE replies"))
                
                # 4. 重命名新表
                conn.execute(db.text("ALTER TABLE replies_new RENAME TO replies"))
                
                # 5. 重新创建索引
                conn.execute(db.text("CREATE INDEX ix_replies_post ON replies(post)"))
                conn.execute(db.text("CREATE INDEX ix_replies_user ON replies(user)"))
                conn.execute(db.text("CREATE INDEX ix_replies_parent ON replies(parent)"))
                
                conn.commit()
                
                print("✅ 迁移完成！replies表的post字段现在可以为空")
                
                # 验证结果
                result = conn.execute(db.text("PRAGMA table_info(replies)"))
                columns = result.fetchall()
                
                print("\n📋 迁移后的replies表结构：")
                for col in columns:
                    print(f"   {col[1]} - {col[2]} - nullable: {not col[3]}")
                
                # 检查数据完整性
                result = conn.execute(db.text("SELECT COUNT(*) FROM replies"))
                count = result.fetchone()[0]
                print(f"\n📊 数据完整性检查：replies表共有 {count} 条记录")
            
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate_make_post_nullable()
