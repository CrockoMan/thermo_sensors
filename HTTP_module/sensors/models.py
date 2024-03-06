from datetime import datetime

from fastapi.openapi.models import Schema
from sqlalchemy import Column, Integer, String, Float, DateTime, TIMESTAMP, \
    ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Sensor(Base):
    """Описание датчиков."""
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    secretkey = Column(String, nullable=False)
    description = Column(String)

    sensor_data_relation = relationship('SensorData',
                                        back_populates="sensor_relation")



class SensorData(Base):
    """Данные датчиков."""
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)
    sensor_value = Column(Float, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow())
    sensor = Column(Integer, ForeignKey('sensor.id'))

    sensor_relation = relationship('Sensor',
                                   back_populates="sensor_data_relation")
