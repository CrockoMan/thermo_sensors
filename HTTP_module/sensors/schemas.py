from typing import Optional

from pydantic import BaseModel


class SensorSchema(BaseModel):
    id: int
    name: str
    secretkey: str
    description: Optional[str]

    class Config:
        orm_mode = True


class SensorCreateSchema(BaseModel):
    name: str
    secretkey: str
    description: Optional[str]


class SensorData(BaseModel):
    pass