from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings
from app.database.base import Base  # your models should be imported in this Base
from app.models import chat  # make sure all models are imported

# Load .env for local dev
from dotenv import load_dotenv
load_dotenv()

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Async URL from .env
DATABASE_URL = settings.DATABASE_URL

# Convert asyncpg driver to psycopg2 for sync migration
if "postgresql+asyncpg" in DATABASE_URL:
    sync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
else:
    sync_url = DATABASE_URL

config.set_main_option("sqlalchemy.url", sync_url)

# Set metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
