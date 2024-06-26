from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from thermo.settings import SENSOR_MAX_VALUE, SENSOR_MIN_VALUE
from users.models import User

MAX_LENGTH = 20


class Location(models.Model):
    name = models.CharField('Наименование',max_length=50)
    description = models.TextField('Описание')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='location_user'
                             # related_name='location'
                             )

    class Meta:
        verbose_name = 'Расположение'
        verbose_name_plural = 'Расположение'
        ordering = ('id',)

    def __str__(self):
        return self.name[:MAX_LENGTH]


class Sensor(models.Model):
    name = models.CharField('Наименование',max_length=50)
    description = models.TextField('Описание')
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE,
                                 related_name='location'
                                 )

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчик'
        ordering = ('id',)

    def __str__(self):
        return self.name[:MAX_LENGTH]


class SensorData(models.Model):
    sensor_value = models.DecimalField('Значение',
                                       max_digits=5,
                                       decimal_places=2)
    sensor_datetime = models.DateTimeField('Добавлено',
                                           auto_now_add=True)
    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name='sensor'
                               )

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ('id',)

    def __str__(self):
        return f'{self.sensor_value} {self.sensor_datetime}'


class SensorSettings(models.Model):
    sensor_settings = models.DecimalField('Установка',
                                       max_digits=5,
                                       decimal_places=2,
                                       validators=(
                                           MinValueValidator(
                                               SENSOR_MIN_VALUE,
                                               message=f'min {SENSOR_MIN_VALUE}'
                                           ),
                                           MaxValueValidator(
                                               SENSOR_MAX_VALUE,
                                               message=f'max {SENSOR_MAX_VALUE}'
                                           ),
                                       ),
                                          )
    sensor_datetime = models.DateTimeField('Добавлено',
                                           auto_now_add=True)
    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name='sensor_settings_id'
                               )

    class Meta:
        verbose_name = 'Установка'
        verbose_name_plural = 'Установки'
        ordering = ('id',)

    def __str__(self):
        return f'{self.sensor_settings} {self.sensor_datetime}'
