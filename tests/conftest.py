from datetime import datetime

import pytest

from sensors.models import Location, Sensor


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def registered_user():
    return {'username': 'Автор',
            'password': '<PASSWORD>'}


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def user(django_user_model):
    return django_user_model.objects.create(username='Автор',
                                            password='<PASSWORD>')

@pytest.fixture
def location(user):
    # Создаём объект Location.
    location = Location.objects.create(
        name='Наименование Location',
        description='Подробное описание Location',
        user=user,
    )
    return location


@pytest.fixture
def sensor(location):
    sensor = Sensor.objects.create(name='Наименование',
                                   description='Описание',
                                   location=location
                                   )
    return sensor


@pytest.fixture
def sensor_data(sensor, registered_user):
    return {**registered_user,
            'sensor_id': sensor.id,
            'sensor_data': 25.9
            }
