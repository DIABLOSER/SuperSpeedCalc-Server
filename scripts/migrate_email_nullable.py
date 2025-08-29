#!/usr/bin/env python3
"""
将 my_user.email 改为可空（兼容 SQLite 的表重建策略）。
运行：python scripts/migrate_email_nullable.py
"""

import os
import sys
from sqlalchemy import text, inspect

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from models import db


def is_sqlite(engine):
    return engine.url.get_backend_name() == 'sqlite'


def rebuild_table_sqlite(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if 'my_user' not in tables:
        print('❌ 表 my_user 不存在')
        return

    columns = {c['name'] for c in inspector.get_columns('my_user')}

    # 构造兼容旧库的列集合（可能存在 experence 或 score）
    has_experence = 'experence' in columns and 'experience' not in columns
    has_score = 'score' in columns

    # 目标表结构：email 可空；去掉 score（若仍存在则不复制到新表）；将 experence 以原始名字保留（避免破坏旧库数据），由其他迁移负责重命名
    create_tmp = (
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
        f"{'experence INTEGER DEFAULT 0,' if has_experence else 'experience INTEGER DEFAULT 0,'}"
        "boluo INTEGER DEFAULT 0,"
        "isActive BOOLEAN DEFAULT 1,"
        "admin BOOLEAN DEFAULT 0,"
        "sex INTEGER DEFAULT 1,"
        "birthday DATE"
        ")"
    )

    # 复制语句根据现有列拼装
    select_experience_col = 'experence' if has_experence else 'experience'
    copy_sql = (
        "INSERT INTO my_user_tmp (objectId, createdAt, updatedAt, username, email, mobile, password, avatar, bio, "
        f"{select_experience_col}, boluo, isActive, admin, sex, birthday) "
        "SELECT objectId, createdAt, updatedAt, username, email, mobile, password, avatar, bio, "
        f"{select_experience_col}, boluo, isActive, admin, sex, birthday FROM my_user"
    )

    with engine.begin() as conn:
        print('🔧 正在以 SQLite 表重建方式将 email 改为可空...')
        conn.execute(text(create_tmp))
        conn.execute(text(copy_sql))
        conn.execute(text('DROP TABLE my_user'))
        conn.execute(text('ALTER TABLE my_user_tmp RENAME TO my_user'))
        # 重新创建唯一索引
        conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_username ON my_user (username)'))
        conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_email ON my_user (email)'))
        conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_mobile ON my_user (mobile)'))

    print('✅ SQLite 表重建完成，email 已可为空')


def alter_table_generic(engine):
    # 兼容常见后端（Postgres/MySQL）
    # Postgres: ALTER TABLE ... ALTER COLUMN ... DROP NOT NULL
    # MySQL:   ALTER TABLE ... MODIFY ... NULL
    tried = False
    try:
        tried = True
        sql = 'ALTER TABLE my_user ALTER COLUMN email DROP NOT NULL'
        with engine.begin() as conn:
            print(f'Executing: {sql}')
            conn.execute(text(sql))
        print('✅ email 已可为空 (Postgres 风格)')
        return
    except Exception:
        pass
    try:
        tried = True
        sql = 'ALTER TABLE my_user MODIFY email VARCHAR(100) NULL'
        with engine.begin() as conn:
            print(f'Executing: {sql}')
            conn.execute(text(sql))
        print('✅ email 已可为空 (MySQL 风格)')
        return
    except Exception as e:
        if tried:
            print(f'⚠️ 自动修改失败: {e}')
        raise


def main():
    app = create_app('development')
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if 'my_user' not in tables:
            print('❌ 表 my_user 不存在')
            return

        # 直接尝试 generic 改法，不行则用 SQLite 重建
        try:
            if is_sqlite(engine):
                rebuild_table_sqlite(engine)
            else:
                alter_table_generic(engine)
        except Exception as e:
            print(f'⚠️ 首次尝试失败，将回退到 SQLite 表重建：{e}')
            rebuild_table_sqlite(engine)

        # 验证
        inspector = inspect(engine)
        cols = inspector.get_columns('my_user')
        email_col = next((c for c in cols if c['name'] == 'email'), None)
        if email_col is None:
            raise RuntimeError('迁移后未找到 email 列')
        print('🎉 迁移完成: email 可为空')


if __name__ == '__main__':
    main()


