from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Vehicle(Base):
    __tablename__ = "vehicle"

    v_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    license = Column(String)
    v_type = Column(String)
    colour = Column(String)
    v_class = Column(String)
    c_id = Column(Integer, ForeignKey("client.c_id"))

    owner = relationship("Client", back_populates="vehicles")
