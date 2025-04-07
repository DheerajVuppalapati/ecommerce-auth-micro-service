import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

from app.cores.database import Base 
from app.models import userModel

# Load .env
load_dotenv()

# Alembic config
config = context.config

# Load logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set SQLAlchemy URL from env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:1234@localhost/ecommerceAuth")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
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
