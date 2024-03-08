from sqladmin import ModelView

from sensors.models import Sensor, SensorData


class SensorAdmin(ModelView, model=Sensor):
    column_list = [Sensor.id, Sensor.name, Sensor.sensor_data_relation]
    column_details_exclude_list = ['secretkey',]
    can_delete = False
    name = 'Контроллеры'
    name_plural = 'Контроллер'


class SensorDataAdmin(ModelView, model=SensorData):
    column_list = [SensorData.id,
                   SensorData.sensor_value,
                   SensorData.registered_at,
                   SensorData.sensor_relation]
    # column_details_exclude_list = ['secretkey',]
    can_delete = False
    name = 'Измерения'
    name_plural = 'Измерение'

