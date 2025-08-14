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

# 运行方式：python scripts/migrate_add_user_fields.py

def is_sqlite_engine(engine):
    name = engine.url.get_backend_name()
    return name == 'sqlite'

def make_email_nullable_sqlite(engine):
    # 使用表重建方式将 email 改为可空
    # 1. 创建临时表结构（email 去掉 NOT NULL）
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
        "score INTEGER DEFAULT 0,"
        "experence INTEGER DEFAULT 0,"
        "boluo INTEGER DEFAULT 0,"
        "isActive BOOLEAN DEFAULT 1,"
        "admin BOOLEAN DEFAULT 0,"
        "sex INTEGER DEFAULT 1,"
        "birthday DATE"
        ")"
    )
    # 2. 复制数据（列对应）
    copy_sql = (
        "INSERT INTO my_user_tmp (objectId, createdAt, updatedAt, username, email, mobile, password, avatar, bio, score, experence, boluo, isActive, admin, sex, birthday) "
        "SELECT objectId, createdAt, updatedAt, username, email, mobile, password, avatar, bio, score, experence, boluo, isActive, admin, sex, birthday FROM my_user"
    )
    # 3. 删除旧表并重命名
    drop_old = "DROP TABLE my_user"
    rename_new = "ALTER TABLE my_user_tmp RENAME TO my_user"
    # 4. 重新创建唯一索引
    recreate_unique_sqls = [
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_username ON my_user (username)",
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_email ON my_user (email)",
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_my_user_mobile ON my_user (mobile)",
    ]
    with engine.begin() as conn:
        print("Rebuilding my_user to make email nullable (SQLite)...")
        conn.execute(text(create_tmp_sql))
        conn.execute(text(copy_sql))
        conn.execute(text(drop_old))
        conn.execute(text(rename_new))
        for stmt in recreate_unique_sqls:
            print(f"Executing: {stmt}")
            conn.execute(text(stmt))


def make_email_nullable_generic(engine):
    # 针对支持 ALTER COLUMN 语法的数据库尝试去除 NOT NULL
    # 兼容性取决于后端（MySQL、Postgres 可用不同语法）
    # 先尝试常见语法，失败则提示手动处理
    tried = False
    try:
        tried = True
        sql = "ALTER TABLE my_user ALTER COLUMN email DROP NOT NULL"
        with engine.begin() as conn:
            print(f"Executing: {sql}")
            conn.execute(text(sql))
        return
    except Exception:
        pass
    try:
        tried = True
        sql = "ALTER TABLE my_user MODIFY email VARCHAR(100) NULL"
        with engine.begin() as conn:
            print(f"Executing: {sql}")
            conn.execute(text(sql))
        return
    except Exception as e:
        if tried:
            print(f"Failed to ALTER email nullability automatically: {e}")
        raise


def main():
    app = create_app('development')
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        existing_columns = {col['name'] for col in inspector.get_columns('my_user')}

        # 收集需要执行的 DDL 语句
        statements = []
        if 'admin' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN admin BOOLEAN DEFAULT 0")
        if 'sex' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN sex INTEGER DEFAULT 1")
        if 'birthday' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN birthday DATE")
        if 'mobile' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN mobile VARCHAR(20)")

        # 执行新增列
        try:
            if statements:
                with engine.begin() as conn:
                    for stmt in statements:
                        print(f"Executing: {stmt}")
                        conn.execute(text(stmt))
            else:
                print("No new columns to add.")
        except Exception as e:
            print(f"Column migration failed: {e}")
            raise

        # 将 email 改为可空
        try:
            # 检查当前 email 是否 NOT NULL（SQLite 无法从 inspector 直接判断约束，这里直接尝试）
            if is_sqlite_engine(engine):
                make_email_nullable_sqlite(engine)
            else:
                make_email_nullable_generic(engine)
            print("Email column is now nullable.")
        except Exception as e:
            print(f"Failed to make email nullable automatically: {e}")
            # 不中断，以免阻塞其他改动

        # 为 mobile 创建唯一索引（若不存在）
        try:
            indexes = inspector.get_indexes('my_user')
            has_mobile_unique_index = False
            for idx in indexes:
                cols = idx.get('column_names') or []
                if idx.get('unique') and cols == ['mobile']:
                    has_mobile_unique_index = True
                    break
                # 放宽匹配：mobile 在唯一索引列中
                if idx.get('unique') and 'mobile' in cols:
                    has_mobile_unique_index = True
                    break

            if not has_mobile_unique_index:
                index_name = 'ux_my_user_mobile'
                create_index_sql = f"CREATE UNIQUE INDEX {index_name} ON my_user (mobile)"
                with engine.begin() as conn:
                    print(f"Executing: {create_index_sql}")
                    conn.execute(text(create_index_sql))
                print("Unique index on 'mobile' created.")
            else:
                print("Unique index for 'mobile' already exists. Skipping.")
        except Exception as e:
            print(f"Index creation failed: {e}")
            raise

        print("Migration completed successfully.")

if __name__ == '__main__':
    main() 