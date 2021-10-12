import json
import uuid
from datetime import datetime

from sqlalchemy import *
from app.models.nodes import Base


class ExternalResources(Base):
    __tablename__ = 'external_resource'
    id = Column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String(128))
    instance_type = Column(String(32))  # 资源类型
    desc = Column(String(128))  # 描述
    buy_at = Column(DateTime)  # 购买时间
    expire_at = Column(DateTime)  # 到期时间
    status = Column(String(32))
    sms_status = Column(Boolean, default=True)  # 短信发送状态
    created_at = Column(DateTime, default=datetime.now)  # 记录创建的时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间
    alert_level = Column(Enum('1', '2', '3'), nullable=False, default='1')
    alert_disable = Column(Boolean, default=False)
    alert_peoples = Column(Text)  # 告警用户组
    related_objects = Column(Text)  # 关联资源组

    def to_dict(self):
        if not self.alert_peoples:
            self.alert_peoples = ""
        if not self.related_objects:
            self.related_objects = ""
            dic = {
                "id": self.id,
                "name": self.name,
                "instance_type": self.instance_type,
                "desc": self.desc,
                "status": self.status,
                "buy_at": str(self.buy_at),
                "expire_at": str(self.expire_at),
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
                "sms_status": self.sms_status,
                "alert_level": self.alert_level,
                "alert_disable": self.alert_disable,
                "alert_peoples": self.alert_peoples,
                "related_objects": self.related_objects,
            }
            return dic
        else:
            dic = {
                "id": self.id,
                "name": self.name,
                "instance_type": self.instance_type,
                "desc": self.desc,
                "status": self.status,
                "buy_at": str(self.buy_at),
                "expire_at": str(self.expire_at),
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
                "sms_status": self.sms_status,
                "alert_level": self.alert_level,
                "alert_disable": self.alert_disable,
                "alert_peoples": self.alert_peoples,
                "related_objects": eval(json.loads(self.related_objects)),
            }
            return dic
