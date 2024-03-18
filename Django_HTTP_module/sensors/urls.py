from django.urls import path

from sensors import views

app_name = 'sensors'

urlpatterns = [
    path('', views.sensor_index, name='sensor_index'),
]
