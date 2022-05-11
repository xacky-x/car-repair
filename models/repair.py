#!/usr/bin/python3.9
# @Time    : 2022/5/4 13:38
# @Author  : Cetacean
# @File    : repair.py

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
import models


class Repair(Base):
    __tablename__ = "repair"

    r_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    r_type = Column(String(20), nullable=False, comment="维修类型")
    r_class = Column(String(20), comment="作业分类")
    payment = Column(String(20), comment="结算方式")
    mileage = Column(Float, comment="进场里程数")
    fuel = Column(Float, comment="进场油量")
    approach_time = Column(DateTime, comment="进场时间")
    failure = Column(Text, comment="故障描述")
    completion_time = Column(Date, comment="预计完工时间")
    date = Column(Date, comment="登记日期")
    cost = Column(Float, comment="费用")
    s_id = Column(Integer, ForeignKey('user.id'), comment="业务员编号")
    v_id = Column(Integer, ForeignKey('vehicle.v_id'), comment="车架号")

    r_salesman = relationship('User', back_populates='s_repair')
    r_vehicle = relationship('Vehicle', back_populates='v_repair')

    r_order = relationship('Order', back_populates='o_repair')
