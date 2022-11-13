from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('fbv-index', views.index_view, name='fbv-index'),
    # path('cbv-index', TemplateView.as_view(template_name='index.html', extra_context={'name': 'hasan'}), name='cbv-index'),
    path('cbv-index', views.IndexView.as_view(), name='cbv-index'),
]