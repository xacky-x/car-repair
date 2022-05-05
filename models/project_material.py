#!/usr/bin/python3.9
# @Time    : 2022/5/5 17:14
# @Author  : Cetacean
# @File    : project_material.py


from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
import models


class PMaterial(Base):
    __tablename__ = "pmaterial"

    mt_id = Column(Integer, ForeignKey('material.mt_id'), primary_key=True, comment="材料编号", index=True)
    p_id = Column(Integer, ForeignKey('project.p_id'), primary_key=True, comment="维修项目编号", index=True)
    num = Column(Integer, comment="数量")

    pm_material = relationship('Material', back_populates='m_pm')
    pm_project = relationship('Project', back_populates='p_pm')
