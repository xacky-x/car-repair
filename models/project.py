from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
import models


class Project(Base):
    __tablename__ = "project"

    p_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    p_name = Column(String(20), comment="维修项目名称")

    p_order = relationship('Order', back_populates='o_project')
    p_pm = relationship('PMaterial', back_populates='pm_project')
