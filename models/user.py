from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String)
    password = Column(String)
    name = Column(String)
    m_type = Column(String)
    m_hour = Column(Float)
    is_administrator = Column(Boolean, default=False)
    is_maintenance = Column(Boolean)

    s_repair = relationship('Repair', back_populates="r_salesman")
