from typing import Optional

from fastapi import APIRouter, HTTPException

from sensors.dao import SensorDAO
from sensors.schemas import SensorSchema, SensorCreateSchema

router_sensors = APIRouter(prefix="/sensors", tags=["sensors"])


@router_sensors.get('/{id}')
async def get_sensors(id: int) -> SensorSchema:
    result = await SensorDAO.find_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    print(f'------------> {result}')
    return result


@router_sensors.delete('/{id}')
async def delete(id: int):
    result = await SensorDAO.delete(id)
    print(f'------------> {result}')

@router_sensors.get('')
async def get_sensors() -> list[SensorSchema]:
    result = await SensorDAO.find_all()
    return result


@router_sensors.post('')
async def add_sensor(sensor: SensorCreateSchema) -> SensorSchema:
    new_sensor = await SensorDAO.add(name=sensor.name,
                                     secretkey=sensor.secretkey,
                                     description=sensor.description)
    return new_sensor
