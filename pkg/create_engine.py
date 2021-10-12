from sqlalchemy import create_engine
from pkg.util.setting import setting


def create_myengine():
    engine = create_engine(
        setting.get_mysql_config(),
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=-1
    )
    return engine
