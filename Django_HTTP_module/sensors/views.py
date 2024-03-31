from django.db.models import F
from django.shortcuts import get_object_or_404, render

from sensors.models import Sensor, SensorData, SensorSettings


def get_sensors(id=None, request=None):
    """Получить все записи Sensors"""
    if request.user.is_authenticated:
        sensors = Sensor.objects.filter(
            location__user=request.user
        ).select_related('location').order_by('id')
    else:
        sensors = Sensor.objects.select_related('location').order_by('id')
    if id is not None:
        sensors = sensors.filter(id=id)

    return sensors


def get_sensor_last_settings(sensor):
    settings = SensorSettings.objects.filter(sensor=sensor).order_by(
        '-sensor_datetime')[:1]
    if settings:
        # settings = settings[0].sensor_settings
        return settings
    return None


def sensor_index(request):
    """Главная страница."""
    sensors = get_sensors(request=request)
    return render(request, 'base.html',
                  {'sensors': sensors})
    # return render(request, 'sensors/sensors.html', {'sensors': sensors})


def sensor_detail(request, sensor_id=None):
    """Вывод данных одного сенсора."""
    if request.user.is_authenticated:
        sensor = get_object_or_404(Sensor, id=sensor_id, location__user = request.user)
    else:
        sensor = get_object_or_404(Sensor, id=sensor_id)
    sensors = get_sensors(request=request)
    sensor_settings = get_sensor_last_settings(sensor)
    # sensor_data = SensorData.objects.filter(sensor=sensor.id).order_by(
    #     '-sensor_datetime')[:10]

    sensor_data = SensorData.objects.raw(
"""SELECT sensors_sensordata.id, 
		sensors_sensordata.sensor_id,
		sensors_sensordata.sensor_value, 
		sensors_sensordata.sensor_datetime,
		(SELECT sensors_sensorsettings.sensor_settings
		FROM sensors_sensorsettings
		WHERE sensors_sensorsettings.sensor_datetime<sensors_sensordata.sensor_datetime
			  AND sensors_sensorsettings.sensor_id=sensors_sensordata.sensor_id
		ORDER BY sensors_sensorsettings.sensor_datetime DESC
		LIMIT 1) 
		    AS sensor_target_setting_value,
		(SELECT sensors_sensorsettings.sensor_datetime
		FROM sensors_sensorsettings
		WHERE sensors_sensorsettings.sensor_datetime<sensors_sensordata.sensor_datetime
			  AND sensors_sensorsettings.sensor_id=sensors_sensordata.sensor_id
		ORDER BY sensors_sensorsettings.sensor_datetime DESC
		LIMIT 1) 
		    AS sensor_target_setting_datetime
FROM sensors_sensordata
JOIN sensors_sensor ON sensors_sensor.id=sensors_sensordata.sensor_id
WHERE sensors_sensor.id=%s
ORDER BY sensors_sensordata.sensor_datetime DESC
LIMIT 10
;""", [sensor_id])

    return render(request, 'sensors/measurement.html',
                  {'sensor_data': sensor_data,
                   'sensor_settings': sensor_settings,
                   'sensors': sensors})
