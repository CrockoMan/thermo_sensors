from django.shortcuts import render

from sensors.models import Sensor


def get_sensors():
    """Получить все записи Sensors"""
    # posts = Sensor.objects.select_related('category',
    #                                     'location',
    #                                     'author').order_by('-pub_date')
    sensors = Sensor.objects.select_related('location').order_by('id')
    # if sensors_count:
    #     return posts.annotate(comment_count=Count('comments'))

    return sensors


def sensor_index(request):
    """Главная страница."""
    sensors = get_sensors()
    return render(request, 'base.html', {'sensors': sensors})
    # return render(request, 'sensors/sensors.html', {'sensors': sensors})

