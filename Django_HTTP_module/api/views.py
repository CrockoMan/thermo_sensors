from http import HTTPStatus

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import (SensorSerializer, LocationSerializer,
                             AddSensorDataSerializer)
from sensors.models import Sensor, Location
from users.models import User


# class SensorViewSet(viewsets.ReadOnlyModelViewSet):
class SensorViewSet(viewsets.ModelViewSet):
    """(GET): получить список всех датчиков."""

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    http_method_names = ['get', 'post', '']

    @action(methods=['post'], url_path='measurement', detail=False)
    def add_sensor_data(self, request):
        """Записать новое измерение."""
        # user = request.user
        serializer = AddSensorDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'Sensor': 'Measurement save'},
                        status=HTTPStatus.OK
                        )


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """(GET): получить список всех датчиков."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
