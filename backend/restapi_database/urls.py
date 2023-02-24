from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('add-simplification/', views.post_simplification),
    path('', views.post_feedback),
    path('database-info/', views.get),
]
