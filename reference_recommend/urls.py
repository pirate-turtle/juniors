from django.urls import path
from .views import LinkListView, LinkCreateView, LinkUpdateView, LinkDeleteView, MyLinkListView

app_name = 'recommend'
urlpatterns = [
    path('link/', LinkListView.as_view(), name='link_list'),
    path('link/create/', LinkCreateView.as_view(), name='link_create'),
    path('link/<int:pk>/update/', LinkUpdateView.as_view(), name='link_update'),
    path('link/<int:pk>/delete/', LinkDeleteView.as_view(), name='link_delete'),
    path('my_link/', MyLinkListView.as_view(), name='my_link')
]