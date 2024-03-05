from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, Integer, String, TIMESTAMP,
                        ForeignKey, JSON, Boolean)

metadata = MetaData()

# role = Table(
#     'sensor',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String, nullable=False),
# )
#
# user = Table(
#     'sensor_data',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('sensor_id', Integer, ForeignKey('sensor.id')),
#     Column('temp', Integer, nullable=False),
#     Column('registered_at', TIMESTAMP, default=datetime.utcnow()),
#     # Column('hashed_password', String,nullable=False),
#     # Column('registered_at', TIMESTAMP, default=datetime.utcnow()),
#     # Column('is_active', Boolean, default=True, nullable=False),
#     # Column('is_superuser', Boolean, default=True, nullable=False),
#     # Column('is_verified', Boolean, default=True, nullable=False),
# )
