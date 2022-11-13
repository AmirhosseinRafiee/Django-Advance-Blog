from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from . import views

app_name = "blog"

urlpatterns = [
    # path('cbv-index', TemplateView.as_view(template_name='index.html', extra_context={'name': 'hasan'}), name='cbv-index'),
    path('cbv-index', views.IndexView.as_view(), name='cbv-index'),
    # path('go-to-geeksforgeeks', RedirectView.as_view(url="https://geeksforgeeks.org/"), name='redirect-to-geeksforgeeks'),
    # path('go-to-cbv-index', RedirectView.as_view(pattern_name="blog:cbv-index"), name='redirect-to-cbv-index'),
    path('go-to-geeksforgeeks', views.RedirectToGeeks.as_view(), name='redirect-to-geeksforgeeks'),
]