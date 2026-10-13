"""只读取专用开发库变量；不在文件中保存密码或URL。"""
from alembic import context

from learning_app.storage import Base, build_engine, database_url

engine = build_engine(database_url())
with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()
engine.dispose()
