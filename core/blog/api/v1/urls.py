from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    # path('post/', views.post_list, name='post-list'),
    path('post/', views.PostListView.as_view(), name='post-list'),
    # path('post/<int:id>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]