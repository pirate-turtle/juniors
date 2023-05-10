from django.urls import path
from .views import LinkListView, LinkCreateView

app_name = 'recommend'
urlpatterns = [
    path('link/', LinkListView.as_view(), name='link_list'),
    path('registration/', LinkCreateView.as_view(), name='create')
]