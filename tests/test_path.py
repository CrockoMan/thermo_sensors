from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_save_measurement_sensor(client, user, location, sensor, sensor_data):
    """Тест записи некорректных данных."""
    url = reverse('api:sensors-list')
    response = client.post(url, sensor_data, format='json')
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_api_sensors_page_availability_for_anonymous_user(client):
    # Адрес страницы получаем через reverse():
    url = reverse('api:sensors-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_admin_page_availability_for_anonymous_user(client):
    # Адрес страницы получаем через reverse():
    url = reverse('sensors:sensor_index')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skip(reason='Переадресация не работает, исправляю')
def test_home_availability_for_anonymous_user(client):
    # Адрес страницы получаем через reverse():
    url = reverse('localhost:admin')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
