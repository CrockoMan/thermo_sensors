from http import HTTPStatus

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import (SensorSerializer, LocationSerializer,
                             AddSensorDataSerializer,
                             AddSensorSettingsSerializer)
from sensors.models import Sensor, Location, SensorData, SensorSettings


class SensorViewSet(viewsets.ModelViewSet):
    """Датчики."""

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    http_method_names = ['get', 'post', '']

    @action(methods=['post'], url_path='measurement', detail=False)
    def add_sensor_data(self, request):
        """Записать новое измерение."""

        serializer = AddSensorDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sensor_id = int(serializer.validated_data.get('sensor_id'))
        sensor_data = float(serializer.validated_data.get('sensor_data'))
        try:
            sensor = Sensor.objects.get(id=sensor_id)
            SensorData.objects.create(sensor_value=sensor_data,
                                      sensor=sensor)
        except Exception as e:
            return Response({'Error': f'Data save error {e}'},
                            status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response({'Sensor': 'Measurement saved'},
                        status=HTTPStatus.OK)

    @action(methods=['post', 'get'], url_path='settings/(?P<pk>[^/.]+)?',
            detail=False)
    def sensor_settings(self, request, pk):
        """Запись и чтение уставок датчика."""
        sensor_id = int(pk)
        sensor = get_object_or_404(Sensor, id=sensor_id)
        if self.request.method == "POST":
            serializer = AddSensorSettingsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # sensor_id = int(serializer.validated_data.get('sensor_id'))
            sensor_settings = float(
                serializer.validated_data.get('sensor_settings')
            )
            try:
                sensor = get_object_or_404(Sensor, id=sensor_id)
                SensorSettings.objects.create(sensor_settings=sensor_settings,
                                              sensor=sensor)
            except Exception as e:
                return Response({'Error': f'Data save error {e}'},
                                status=HTTPStatus.INTERNAL_SERVER_ERROR)

            return Response({'Sensor': 'Settings saved'},
                            status=HTTPStatus.OK)
        if self.request.method == "GET":
            settings = SensorSettings.objects.order_by(
                '-sensor_datetime').filter(sensor=sensor)
            if settings:
                return Response({'setting': settings[0].sensor_settings},
                                status=HTTPStatus.OK)
        return Response({'Error': 'Nothing to get'},
                        status=HTTPStatus.NO_CONTENT)


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """(GET): получить список всех датчиков."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
