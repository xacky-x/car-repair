from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Client(Base):
    __tablename__ = "client"

    c_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    c_name = Column(String)
    c_p = Column(String)
    discount = Column(Float)
    contact = Column(String)
    phone = Column(String)

    vehicles = relationship("Vehicle", back_populates="owner")
