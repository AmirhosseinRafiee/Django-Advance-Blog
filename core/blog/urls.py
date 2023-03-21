from django.urls import path, include

# from django.views.generic import TemplateView, RedirectView
from . import views

app_name = "blog"

urlpatterns = [
    # path('cbv-index', TemplateView.as_view(template_name='index.html', extra_context={'name': 'hasan'}), name='cbv-index'),
    path("index/", views.IndexView.as_view(), name="index"),
    # path('go-to-geeksforgeeks', RedirectView.as_view(url="https://geeksforgeeks.org/"), name='redirect-to-geeksforgeeks'),
    # path('go-to-cbv-index', RedirectView.as_view(pattern_name="blog:cbv-index"), name='redirect-to-cbv-index'),
    path(
        "go-to-geeksforgeeks/",
        views.RedirectToGeeks.as_view(),
        name="redirect-to-geeksforgeeks",
    ),
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", views.PostEditView.as_view(), name="post-edit"),
    path(
        "post/<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="post-delete",
    ),
    path("api/v1/", include("blog.api.v1.urls")),
]
