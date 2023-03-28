from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("post", views.PostViewSet, basename="post")
router.register("category", views.CategoryViewSet, basename="category")

# urlpatterns = [
#     # path('post/', views.post_list, name='post-list'),
#     # path('post/<int:id>/', views.post_detail, name='post-detail'),
#     # path('post/', views.PostListView.as_view(), name='post-list'),
#     # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
#     # path('post/', views.PostViewSet.as_view({'get':'list'}), name='post-list'),
#     # path('post/<int:pk>/', views.PostViewSet.as_view({'get':'retrieve'}), name='post-detail'),
# ]

urlpatterns = [path("weather/", views.WeatherApiView.as_view(), name="weather")]

urlpatterns += router.urls
