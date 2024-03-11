from django.db import models

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
