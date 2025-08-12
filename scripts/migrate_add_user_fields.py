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

def main():
    app = create_app('development')
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        existing_columns = {col['name'] for col in inspector.get_columns('my_user')}

        statements = []
        if 'admin' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN admin BOOLEAN DEFAULT 0")
        if 'sex' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN sex INTEGER DEFAULT 1")
        if 'birthday' not in existing_columns:
            statements.append("ALTER TABLE my_user ADD COLUMN birthday DATE")

        if not statements:
            print("All required columns already exist. No changes needed.")
            return

        try:
            with engine.begin() as conn:
                for stmt in statements:
                    print(f"Executing: {stmt}")
                    conn.execute(text(stmt))
            print("Migration completed successfully.")
        except Exception as e:
            print(f"Migration failed: {e}")
            raise

if __name__ == '__main__':
    main() 