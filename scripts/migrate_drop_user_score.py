#!/usr/bin/env python3
"""
数据库迁移脚本：从 my_user 表中删除 score 列
适配 SQLite（通过表重建）和其他数据库（优先使用 ALTER TABLE DROP COLUMN）。
运行方式：python scripts/migrate_drop_user_score.py
"""

import os
import sys
from sqlalchemy import text, inspect

# 确保可以从项目根目录导入 app
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from models import db


def is_sqlite_engine(engine):
    return engine.url.get_backend_name() == 'sqlite'


def drop_score_sqlite(engine):
    """通过重建表的方式在 SQLite 中删除 score 列。"""
    inspector = inspect(engine)
    columns = [c['name'] for c in inspector.get_columns('my_user')]
    if 'score' not in columns:
        print("✅ 'score' 列不存在，跳过重建")
        return

    # 目标表结构：移除 score 列
    create_tmp_sql = (
        "CREATE TABLE my_user_tmp ("
        "objectId VARCHAR(20) NOT NULL PRIMARY KEY,"
        "createdAt DATETIME NOT NULL,"
        "updatedAt DATETIME NOT NULL,"
        "username VARCHAR(50) NOT NULL,"
        "email VARCHAR(100),"
        "mobile VARCHAR(20),"
        "password VARCHAR(255) NOT NULL,"
        "avatar VARCHAR(255),"
        "bio TEXT,"
        "experience INTEGER DEFAULT 0,"
        "boluo INTEGER DEFAULT 0,"
        "isActive BOOLEAN DEFAULT 1,"
        "admin BOOLEAN DEFAULT 0,"
        "sex INTEGER DEFAULT 1,"
        "birthday DATE"
        ")"
    )

    # 将数据复制到新表（不包含 score 列）
    copy_sql = (
        "INSERT INTO my_user_tmp (objectId, createdAt, updatedAt, username, email, mobile, password, avatar, bio, experience, boluo, isActive, admin, sex, birthday) "
        "SELECT objectId, createdAt, updatedAt, username, email, mobile, password, avatar, bio, experience, boluo, isActive, admin, sex, birthday FROM my_user"
    )

    # 删除旧表并重命名
    drop_old = "DROP TABLE my_user"
    rename_new = "ALTER TABLE my_user_tmp RENAME TO my_user"

    # 重新创建唯一索引
    recreate_unique_sqls = [
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_username ON my_user (username)",
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_email ON my_user (email)",
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_mobile ON my_user (mobile)",
    ]

    with engine.begin() as conn:
        print("🔧 正在重建 my_user 表以删除 'score' 列（SQLite）...")
        conn.execute(text(create_tmp_sql))
        conn.execute(text(copy_sql))
        conn.execute(text(drop_old))
        conn.execute(text(rename_new))
        for stmt in recreate_unique_sqls:
            print(f"Executing: {stmt}")
            conn.execute(text(stmt))
    print("✅ SQLite 表重建完成，已删除 'score' 列")


def drop_score_generic(engine):
    """在支持的数据库中直接删除列，失败则抛出异常。"""
    sql = "ALTER TABLE my_user DROP COLUMN score"
    with engine.begin() as conn:
        print(f"Executing: {sql}")
        conn.execute(text(sql))
    print("✅ 已通过 ALTER TABLE 删除 'score' 列")


def main():
    app = create_app('development')
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)

        tables = inspector.get_table_names()
        if 'my_user' not in tables:
            print("❌ 表 my_user 不存在，退出")
            return

        existing_columns = {col['name'] for col in inspector.get_columns('my_user')}
        if 'score' not in existing_columns:
            print("✅ 'score' 列已不存在，无需迁移")
            return

        try:
            if is_sqlite_engine(engine):
                drop_score_sqlite(engine)
            else:
                drop_score_generic(engine)
        except Exception as e:
            print(f"⚠️ 直接删除列失败或不支持，尝试使用重建方式：{e}")
            drop_score_sqlite(engine)

        # 验证结果
        inspector = inspect(engine)
        columns_after = {col['name'] for col in inspector.get_columns('my_user')}
        assert 'score' not in columns_after, "迁移后仍存在 'score' 列"
        print("🎉 迁移完成，'score' 列已移除")


if __name__ == '__main__':
    main()


