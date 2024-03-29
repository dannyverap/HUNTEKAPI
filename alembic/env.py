from src.user_profile.models import UserProfile
from src.company_profile.models import CompanyProfile
from src.roles.models import Role, user_roles
from src.users.models import User
from src.token.models import Token
from src.interviews.models import Interviews
from src.job_offers.models import JobOffer
from src.job_applications.models import JobApplication
import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
db_url_escaped = os.environ.get('SQLALCHEMY_DATABASE_URI')
config.set_main_option('sqlalchemy.url', db_url_escaped)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# Search in full project
sys.path = ['', '..'] + sys.path[1:]
# Include main Model
target_metadata = User.metadata
target_metadata = Role.metadata
target_metadata = user_roles.to_metadata
target_metadata = Token.metadata
target_metadata = User.metadata
target_metadata = UserProfile.metadata
target_metadata = CompanyProfile.metadata
target_metadata = Interviews.metadata
target_metadata = JobOffer.metadata
target_metadata = JobApplication.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = db_url_escaped
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
    run_migrations_online()
