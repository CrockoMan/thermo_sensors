# Generated by Django 3.2.3 on 2024-03-16 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='sensors.location'),
        ),
        migrations.CreateModel(
            name='SensorSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_settings', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Установка')),
                ('sensor_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_settings', to='sensors.sensor')),
            ],
            options={
                'verbose_name': 'Установка',
                'verbose_name_plural': 'Установки',
                'ordering': ('id',),
            },
        ),
    ]
