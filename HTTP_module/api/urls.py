from django.urls import path, include
from rest_framework import routers

from api.views import SensorViewSet, LocationViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('sensors', SensorViewSet, basename='sensors')
router_v1.register('locations', LocationViewSet, basename='location')
# router_v1.register('posts/(?P<post_id>\\d+)/comments',
#                    CommentViewSet,
#                    basename='comments')
# router_v1.register('groups', GroupViewSet, basename='groups')

urlpatterns = [
    # path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]
