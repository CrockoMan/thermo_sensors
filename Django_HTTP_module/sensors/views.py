from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from sensors.models import Location, Sensor, SensorData, SensorSettings
from thermo.settings import SENSOR_MAX_VALUE, SENSOR_MIN_VALUE


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

def check_min_max_value(value):
    return value >= SENSOR_MIN_VALUE and value <= SENSOR_MAX_VALUE


def add_new_sensor(request, location, point_name, target, period):
    location = Location.objects.create(name=location, user=request.user)
    print('Location={location')
    sensor = Sensor.objects.create(name=point_name, location=location)
    print('sensor={sensor')
    sensor_settings = SensorSettings.objects.create(sensor=sensor,
                                                    sensor_settings=target)
    print('sensor_settings={sensor_settings')
    return sensor


def add_sensor(request):
    sensors = get_sensors(request=request)
    error = ''
    if request.method == 'POST' and request.user.is_authenticated:
        location = request.POST.get('location', '').strip()
        point_name = request.POST.get('point_name', '').strip()
        target = request.POST.get('target', '')
        period = request.POST.get('period', '')
        print('Данные получены')
        if (location != ''
            and point_name != ''
            and target != ''
            and period != ''
            and check_min_max_value(int(target))
        ):
            print('Данные отправлены на сохранение')
            new_sensor = add_new_sensor(request=request,
                                        location=location,
                                        point_name=point_name,
                                        target=int(target),
                                        period=int(period))
            return redirect('sensors:sensor_detail',
                            sensor_id=new_sensor.id)
        else:
            error = 'Проверьте параметры'
    return render(request, 'sensors/add_sensor.html',
                  {'sensors': sensors,
                   'error': error})


def sensor_detail(request, sensor_id=None):
    """Вывод данных одного сенсора."""
    if request.user.is_authenticated:
        sensor = get_object_or_404(Sensor,
                                   id=sensor_id,
                                   location__user=request.user
                                   )
    else:
        sensor = get_object_or_404(Sensor, id=sensor_id)

    if request.method == 'POST' and request.user.is_authenticated:
        new_point_name = request.POST.get('new_point_name', '').strip()
        new_settings = request.POST.get('new_settings', '')

        if sensor.name != new_point_name:
            Sensor.objects.filter(id=sensor_id).update(name=new_point_name)
        if new_settings and check_min_max_value(int(new_settings)):
            SensorSettings.objects.create(sensor_settings=int(new_settings),
                                          sensor=sensor)

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
                   'sensors': sensors,
                   'sensor_id': sensor_id})
