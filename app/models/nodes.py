import json
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Nodes(Base):
    __tablename__ = 'nodes'
    id = Column(String(64), primary_key=True)
    cloud_type = Column(String(32))  # 所属云类型(云平台)
    instance_type = Column(String(64))  # 实例规格
    cpu = Column(Integer)  # CPU
    mem_size = Column(Integer)  # memsize
    account_name = Column(String(64))   # 账号名称
    hostname = Column(String(32))  # 主机名称
    os = Column(Text)  # 镜像信息
    ipaddress_lan = Column(String(64))  # 内网ip
    ipaddress_wan = Column(String(64))  # 公网ip
    status = Column(String(32), default='FREEZING')
    platform = Column(Text)  # 其他信息(metadata)
    buy_at = Column(DateTime)  # 购买时间
    expire_at = Column(DateTime)  # 主机到期时间
    created_at = Column(DateTime, default=datetime.now)  # 记录创建的时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间
    sms_status = Column(Boolean, default=True)  # 短信发送状态
    body_hash = Column(String(128))
    alert_level = Column(Enum('1', '2', '3'), nullable=False, default='1')
    alert_disable = Column(Boolean, default=False)
    alert_peoples = Column(Text)  # 告警用户组
    network_id = Column(String(128), ForeignKey('network.id', ondelete='CASCADE'))  # 关联的共享带宽id

    def to_dict(self):
        if not self.alert_peoples:
            self.alert_peoples = ""
        dic = {
            "id": self.id,
            "cloud_type": self.cloud_type,
            "instance_type": self.instance_type,
            "hostname": self.hostname,
            "os": self.os,
            "ipaddress_lan": self.ipaddress_lan,
            "ipaddress_wan": self.ipaddress_wan,
            "status": self.status,
            "platform": self.platform,
            "buy_at": str(self.buy_at),
            "expire_at": str(self.expire_at),
            "cpu": self.cpu,
            "mem_size": self.mem_size,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at.strftime("%Y-%m-%d %H:%M:%S")),
            "body_hash": self.body_hash,
            "alert_level": self.alert_level,
            "alert_disable": self.alert_disable,
            "sms_status": self.sms_status,
            "alert_peoples": self.alert_peoples,
            "network_id": self.network_id,
            "account_name": self.account_name,
        }
        return dic
