from rest_framework import serializers

from sensors.models import Sensor, Location, SensorData
from users.models import User

class SensorCommonSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    sensor_id = serializers.IntegerField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        sensor_id = int(data.get('sensor_id'))
        # sensor_data = float(data.get('sensor_data'))

        if not User.objects.filter(username=username).exists():
            print(f'Username {username} does not')
            raise serializers.ValidationError(detail=f'Ошибка {username}')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            print(f'Password {password} incorrect')
            raise serializers.ValidationError(detail=f'Ошибка {username}')

        if (not Sensor.objects.filter(id=sensor_id).exists()
            or not Sensor.objects.get(
                    id=sensor_id).location.user.username == username
        ):
            print(f'Sensor {sensor_id} does not exist')
            raise serializers.ValidationError(detail='Sensor not exists')
        return data


class AddSensorDataSerializer(SensorCommonSerializer):
    """Новое измерение."""

    sensor_data = serializers.FloatField()


class AddSensorSettingsSerializer(SensorCommonSerializer):
    """Новые уставки."""

    sensor_settings = serializers.FloatField()


class SensorDataSerializer(serializers.ModelSerializer):
    """Получение информации о измерениях."""

    class Meta:
        model = SensorData
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(slug_field='name',
                                            read_only=True)
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

    class Meta:
        model = Location
        fields = '__all__'
