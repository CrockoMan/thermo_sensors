from django.shortcuts import render

from sensors.models import Sensor


def get_sensors():
    """Получить все записи Post"""
    # posts = Sensor.objects.select_related('category',
    #                                     'location',
    #                                     'author').order_by('-pub_date')
    sensors = Sensor.objects.select_related('location').order_by('id')
    # if comment_count:
    #     return posts.annotate(comment_count=Count('comments'))

    return sensors


# def get_filtered_post(post=None):
#     """Фильтрация Post"""
#     if post is None:
#         post = get_all_post()
#     return post.filter(
#         is_published=True,
#         pub_date__lte=timezone.now(),
#         category__is_published=True
#     )

def sensor_index(request):
    """Главная страница."""
    sensors = get_sensors()
    return render(request, 'sensors/sensors.html', {'sensors': sensors})

