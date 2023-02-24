from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('options/', views.get_options, name='get_options_readability'),
    path('measure/', views.readability_post, name='readability_post'),
    path('difficult-sentences/', views.difficult_sentences_post, name='difficult_sentences_post'),
]
