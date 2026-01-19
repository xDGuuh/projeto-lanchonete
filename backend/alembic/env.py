import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.models.base import Base
from app.core.config import DATABASE_URL

# -------------------------------------------------------------------
# Garante que o pacote "app" esteja disponível no PYTHONPATH
# -------------------------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

# -------------------------------------------------------------------
# Alembic Config
# -------------------------------------------------------------------
config = context.config

# DATABASE_URL é validada em config.py (fail-fast).
# Este assert é para o type checker (Pylance / MyPy).
assert DATABASE_URL is not None

# Injeta a URL real (Docker / local / Railway)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------------------------
# Metadata para autogenerate
# -------------------------------------------------------------------
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Executa migrations em modo offline.
    Não cria engine; apenas gera SQL.
    """
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
    """
    Executa migrations em modo online.
    Usa engine síncrono (obrigatório para Alembic).
    """
    connectable = engine_from_config(
        # Nunca retorna None → tipagem correta
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
