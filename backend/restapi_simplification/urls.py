from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.post, name='simplification_post'),
    path('file/', views.file_post, name='simplification_file_post'),
    path('options/', views.get_options, name='get_options_simplification'),
]
