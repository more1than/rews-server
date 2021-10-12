import json
from datetime import datetime
from sqlalchemy import String, Column, Integer, Text, DateTime, Enum, Boolean
from app.models.nodes import Base


class NetWorks(Base):
    __tablename__ = 'network'
    id = Column(String(64), primary_key=True)
    cloud_type = Column(String(32))  # 所属云类型(云平台)
    instance_type = Column(String(32))  # 实例规格
    size = Column(Integer)
    account_name = Column(String(64))  # 账号名称
    network_type = Column(String(32))
    valid_ips = Column(Integer)  # 可分配ip数量
    platform = Column(Text)  # 其他信息(metadata)
    buy_at = Column(DateTime)  # 购买时间
    expire_at = Column(DateTime)  # 主机到期时间
    created_at = Column(DateTime, default=datetime.now)  # 记录创建的时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间
    body_hash = Column(String(128))
    sms_status = Column(Boolean, default=True)  # 短信发送状态
    ips = Column(Text)
    alert_level = Column(Enum('1', '2', '3'), nullable=False, default='1')
    alert_disable = Column(Boolean, default=False)
    status = Column(String(32))
    alert_peoples = Column(Text)  # 告警用户组

    def to_dict(self):
        if not self.alert_peoples:
            self.alert_peoples = ""
        dic = {
            "id": self.id,
            "cloud_type": self.cloud_type,
            "instance_type": self.instance_type,
            "network_type": self.network_type,
            "size": self.size,
            "valid_ips": self.valid_ips,
            "platform": json.loads(self.platform),
            "buy_at": str(self.buy_at),
            "expire_at": str(self.expire_at),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
            "body_hash": self.body_hash,
            "sms_status": self.sms_status,
            "alert_level": self.alert_level,
            "alert_disable": self.alert_disable,
            "status": self.status,
            "alert_peoples": self.alert_peoples,
            "account_name": self.account_name,
        }
        return dic
