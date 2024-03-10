from rest_framework import serializers

from sensors.models import Sensor, Location, SensorData


class SensorDataSerializer(serializers.ModelSerializer):
    """Получение информации о произведениях."""


    class Meta:
        model = SensorData
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(read_only=True,
    #                                       slug_field='username')
    location = serializers.SlugRelatedField(slug_field='name',
                                            read_only=True)
    # sensor_data = SensorDataSerializer(many=True,
    #                                    read_only=True,
    #                                    source='sensor'
    #                                    )
    sensor_data = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        # fields = '__all__'
        fields = ('id', 'name', 'description', 'location', 'sensor_data')

    def get_sensor_data(self, obj):
        message_comments = SensorData.objects.filter(sensor=obj.id)[:1]
        return SensorDataSerializer(message_comments,
                                    source='sensor',
                                    many=True,
                                    read_only=True).data


class LocationSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(read_only=True,
    #                                       slug_field='username')

    class Meta:
        model = Location
        fields = '__all__'
