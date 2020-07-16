from django.urls import path, re_path
from blog import views

app_name = 'blog'
urlpatterns = [
    # Example: /blog/
    path('', views.PostLV.as_view(), name='index'),

    # Example: /blog/post
    path('post/', views.PostLV.as_view(), name='post_list'),

    # Example: /blog/post/django-example
    # slug 필드를 가져다가 주소를 이렇게 만들어달라는 문법. [-\w]는 한글도 쓰기 위해서 넣어준 것.
    # 좋은 문법은 아니다
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDV.as_view(), name='post_detail'),

    # Example: /blog/archive/
    path('archive/', views.PostAV.as_view(), name='post_archive'),

    # Example: /blog/archive/2019
    path('archive/<int:year>', views.PostYAV.as_view(), name='post_year_archive'),

    # Example: /blog/archive/2019/nov/
    path('archive/<int:year>/<int:month>', views.PostMAV.as_view(month_format='%m'), name='post_month_archive'),

    # Example: /blog/archive/2019/nov/10
    path('archive/<int:year>/<int:month>/<int:day>/', views.PostDAV.as_view(month_format='%m'), name='post_day_archive'),

    # Example: /blog/archive/today/
    path('archive/today/', views.PostTAV.as_view(), name='post_today_archive'),

    # Example: /blog/tag/
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),

    # Example: /blog/tag/tagname/
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),

    # Example: /blog/search/
    path('search/', views.SearchFormView.as_view(), name='search'),
]