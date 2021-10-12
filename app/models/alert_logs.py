import uuid
from datetime import datetime
from sqlalchemy import *
from app.models.nodes import Base


class AlertLogs(Base):
    __tablename__ = 'alert_logs'
    id = Column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    created_at = Column(DateTime, default=datetime.now)  # 记录创建的时间
    message = Column(TEXT)  # 告警内容
    alert_peoples = Column(Text)  # 告警用户组
    node_id = Column(String(64))
    disk_id = Column(String(64))
    network_id = Column(String(64))
    external_resource_id = Column(String(64))
    alert_level = Column(Enum('1', '2', '3'), nullable=False, default='1')

    def to_dict(self):
        if not self.alert_peoples:
            self.alert_peoples = ""
        dic = {
            "id": self.id,
            "created_at": str(self.created_at),
            "message": self.message,
            "alert_peoples": self.alert_peoples,
            "node_id": self.node_id,
            "disk_id": self.disk_id,
            "network_id": self.network_id,
            "external_resource_id": self.external_resource_id,
            "alert_level": self.alert_level,
        }
        return dic
