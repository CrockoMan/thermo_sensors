from django.urls import path

from sensors import views

app_name = 'sensors'

posts_urls = [
    # path('create/', views.post_view, name='create_post'),
    # path('<int:post_id>/', views.post_detail, name='post_detail'),
    # path('<int:post_id>/edit/', views.post_view, name='edit_post'),
    # path('<int:post_id>/delete/', views.post_delete, name='delete_post'),
    # path('add_comment/<int:post_id>/',
    #      views.add_comment,
    #      name='add_comment'),
    # path('<int:post_id>/edit_comment/<int:comment_id>/',
    #      views.edit_comment,
    #      name='edit_comment'),
    # path('<int:post_id>/delete_comment/<int:comment_id>/',
    #      views.delete_comment,
    #      name='delete_comment'),
]


urlpatterns = [
    path('', views.sensor_index, name='sensor_index'),
    # path('posts/', include(posts_urls)),
    # path('category/<slug:category_slug>/',
    #      views.category_posts,
    #      name='category_posts'
    #      ),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    # path('profile/<str:username>/', views.profile_view, name='profile'),
]
