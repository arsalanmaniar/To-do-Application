import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Add the current directory to the path so we can import our models
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import our models - avoid loading settings during migration generation
try:
    # Temporarily add the backend directory to the path
    backend_dir = os.path.join(os.path.dirname(parent_dir))
    sys.path.insert(0, backend_dir)

    from backend.models.user import User
    from backend.config.database import Base
except ImportError:
    # Fallback to relative import if the above fails
    try:
        from models.user import User
        from config.database import Base
    except ImportError:
        # Final fallback
        import sys
        import os
        from sqlalchemy import Column, Integer, String, Boolean, DateTime
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        # Define a minimal User model for migration purposes only
        class User(Base):
            __tablename__ = "users"
            id = Column(String, primary_key=True, index=True)
            email = Column(String, unique=True, index=True, nullable=False)
            hashed_password = Column(String, nullable=False)
            is_active = Column(Boolean, default=True)
            created_at = Column(DateTime(timezone=True), nullable=True)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata to our Base class which includes all models
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_db_url():
    """Get database URL from the alembic config or environment."""
    # First try to get from alembic config
    url = config.get_main_option("sqlalchemy.url")
    if url:
        return url

    # Fallback: try to get from environment variables
    import os
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # For migration generation, provide a dummy URL
    # This is safe since we're only generating the migration, not connecting
    return "postgresql://user:pass@localhost/db"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
        # Specify that we don't need transactions for autogenerate
        connectable=None
    )

    # For autogenerate, we don't need to wrap in a transaction
    context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = get_db_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # For actual migration execution, try online mode but provide fallback
    # Use an environment variable to control if we force offline mode
    import os
    if os.environ.get('FORCE_OFFLINE_MIGRATION'):
        run_migrations_offline()
    else:
        run_migrations_online()
