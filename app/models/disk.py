import json
from datetime import datetime
from sqlalchemy import *
from app.models.nodes import Base


class Disks(Base):
    __tablename__ = 'disks'
    id = Column(String(64), primary_key=True)
    cloud_type = Column(String(32))  # 所属云类型(云平台)
    instance_type = Column(String(32))  # 实例规格
    disk_type = Column(String(32))
    account_name = Column(String(64))  # 账号名称
    size = Column(Integer)
    platform = Column(Text)  # 其他信息(metadata)
    buy_at = Column(DateTime)  # 购买时间
    expire_at = Column(DateTime)  # 主机到期时间
    created_at = Column(DateTime, default=datetime.now)  # 记录创建的时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间
    body_hash = Column(String(128))
    sms_status = Column(Boolean, default=True)  # 短信发送状态
    alert_level = Column(Enum('1', '2', '3'), nullable=False, default='1')
    alert_disable = Column(Boolean, default=False)
    node_id = Column(String(64), ForeignKey('nodes.id', ondelete='CASCADE'))
    node_name = Column(String(64))
    status = Column(String(32))
    alert_peoples = Column(Text)  # 告警用户组

    def to_dict(self):
        if not self.alert_peoples:
            self.alert_peoples = ""
        dic = {
            "id": self.id,
            "cloud_type": self.cloud_type,
            "instance_type": self.instance_type,
            "disk_type": self.disk_type,
            "size": self.size,
            "platform": json.loads(self.platform),
            "buy_at": str(self.buy_at),
            "expire_at": str(self.expire_at),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
            "body_hash": self.body_hash,
            "alert_level": self.alert_level,
            "alert_disable": self.alert_disable,
            "sms_status": self.sms_status,
            "node_id": self.node_id,
            "node_name": self.node_name,
            "status": self.status,
            "alert_peoples": self.alert_peoples,
            "account_name": self.account_name,
        }
        return dic
