"""
CLI commands for backend verification and management
"""

import argparse
import sys
from sqlmodel import SQLModel
from sqlalchemy import inspect
from sqlalchemy import create_engine as sql_create_engine
from pydantic_settings import BaseSettings


# Define the Settings class to load environment variables
class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    db_echo: bool = False

    class Config:
        env_file = ".env"


settings = Settings()

# Create the database engine
engine = sql_create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_recycle=300,
)


def check_db_connection():
    """Check if the database connection is working."""
    try:
        # Try to connect and get database information
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("OK Database connection successful")
            return True
    except Exception as e:
        print(f"ERROR Database connection failed: {e}")
        return False


def list_tables():
    """List all tables in the database."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if tables:
            print(f"Found {len(tables)} table(s) in database:")
            for table in tables:
                print(f"  - {table}")
        else:
            print("No tables found in database")

        return tables
    except Exception as e:
        print(f"✗ Failed to list tables: {e}")
        return []


def check_user_task_tables():
    """Check specifically for User and Task tables."""
    tables = list_tables()

    user_exists = 'user' in tables or 'users' in tables
    task_exists = 'task' in tables or 'tasks' in tables

    print("\nTable Status:")
    print(f"  User table: {'OK Exists' if user_exists else 'MISSING'}")
    print(f"  Task table: {'OK Exists' if task_exists else 'MISSING'}")

    return user_exists and task_exists


def main():
    parser = argparse.ArgumentParser(description='Backend verification and management CLI')
    parser.add_argument('command', choices=['check-db-connection', 'list-tables', 'check-tables'],
                       help='Command to execute')

    args = parser.parse_args()

    if not settings.database_url:
        print("✗ DATABASE_URL not found in environment. Please set it in .env file.")
        sys.exit(1)

    print(f"Using database: {settings.database_url.split('@')[-1].split('/')[0] if '@' in settings.database_url else 'Unknown'}")

    if args.command == 'check-db-connection':
        success = check_db_connection()
        sys.exit(0 if success else 1)
    elif args.command == 'list-tables':
        list_tables()
        sys.exit(0)
    elif args.command == 'check-tables':
        success = check_user_task_tables()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()