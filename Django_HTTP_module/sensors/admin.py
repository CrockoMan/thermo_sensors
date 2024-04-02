from django.contrib import admin

from sensors.models import Location, Sensor, SensorData, SensorSettings


@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Sensor)
class Sensor(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'location')
    list_filter = ('name', 'location',)
    search_fields = ('name',)
    ordering = ('id',)

    def location(self, obj):
        return obj

    location.short_description = 'Расположение'


@admin.register(SensorData)
class SensorData(admin.ModelAdmin):
    list_display = ('sensor_value', 'sensor_datetime', 'sensor', 'sensor_id')
    list_filter = ('sensor',)
    # search_fields = ('name',)
    ordering = ('-sensor_datetime',  'sensor_id')

    @admin.display(description='Датчик',)
    def sensor(self, obj):
        return obj


@admin.register(SensorSettings)
class SensorSettings(admin.ModelAdmin):
    list_display = ('sensor_settings', 'sensor_datetime', 'sensor','sensor_id')
    list_filter = ('sensor',)
    # search_fields = ('name',)
    ordering = ('-sensor_datetime', 'sensor_id')

    @admin.display(description='Установка',)
    def sensor(self, obj):
        return obj
