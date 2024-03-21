from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from thermo import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('sensors.urls', namespace='sensor')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
