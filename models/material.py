#!/usr/bin/python3.9
# @Time    : 2022/5/5 17:08
# @Author  : Cetacean
# @File    : material.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
import models


class Material(Base):
    __tablename__ = "material"

    mt_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mt_name = Column(String(20), nullable=False, comment="材料名称")
    mt_cost = Column(Float, comment="材料费")

    m_pm = relationship('PMaterial', back_populates='pm_material')
