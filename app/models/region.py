from sqlalchemy import *
from app.models.nodes import Base


class Region(Base):
    __tablename__ = 'regions'
    regionId = Column(String(255), primary_key=True)
    zoneName = Column(String(255))

    def to_dict(self):
        dic = {
            "regionId": self.regionId,
            "zoneName": self.zoneName
        }
        return dic
