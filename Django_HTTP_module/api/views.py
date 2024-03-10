from rest_framework import viewsets

from api.serializers import SensorSerializer, LocationSerializer
from sensors.models import Sensor, Location


class SensorViewSet(viewsets.ReadOnlyModelViewSet):
    """(GET): получить список всех датчиков."""

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """(GET): получить список всех датчиков."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
