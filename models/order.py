from sqlalchemy import Column, Integer, String, Float,ForeignKey
from sqlalchemy.orm import relationship

from database import Base
import models


class Order(Base):
    __tablename__ = "order"

    o_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    r_id = Column(Integer, ForeignKey('repair.r_id'), comment="维修编号")
    p_id = Column(Integer, ForeignKey('project.p_id'), comment="维修项目编号")
    hour = Column(Float,comment="工时")
    status = Column(Integer,comment="派单状态")
    m_id = Column(Integer, ForeignKey('user.id'), comment="维修员编号")

    o_repair= relationship('Repair', back_populates='r_order')
    o_project = relationship('Project', back_populates='p_order')
    o_maintenance = relationship('User', back_populates='m_order')




