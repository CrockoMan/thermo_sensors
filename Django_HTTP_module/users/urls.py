from django.urls import path, include

from users import views

app_name = 'users'

urlpatterns = [
#    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]