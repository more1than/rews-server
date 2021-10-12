import uuid

from sqlalchemy import *
from app.models.nodes import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String(64), unique=True)
    cloud_type = Column(String(32))  # 所属云类型(云平台)
    api_key = Column(String(64))
    api_sec = Column(String(64))

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "cloud_type": self.cloud_type,
            "api_key": self.api_key,
            "api_sec": self.api_sec,
        }
        return dic
