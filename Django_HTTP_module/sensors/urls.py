from django.urls import include, path

from sensors import views

app_name = 'sensors'

sensor_urls = [
    path('<int:sensor_id>/', views.sensor_detail, name='sensor_detail'),
]


urlpatterns = [
    path('', views.sensor_index, name='sensor_index'),
    path('sensors/', include(sensor_urls)),
]
