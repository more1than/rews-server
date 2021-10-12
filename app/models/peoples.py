import uuid
from datetime import datetime
from sqlalchemy import *
from app.models.nodes import Base


class Peoples(Base):
    __tablename__ = 'peoples'
    id = Column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String(128))
    mail = Column(String(64), unique=True)
    phone = Column(String(64), unique=True)
    im_ding = Column(String(64), unique=True)  # 钉钉账号
    im_wechat = Column(String(64), unique=True)  # 微信账号
    created_at = Column(DateTime, default=datetime.now)  # 记录创建的时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
            "phone": self.phone,
            "im_ding": self.im_ding,
            "im_wechat": self.im_wechat,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
        }
        return dic
