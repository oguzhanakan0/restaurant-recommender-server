from django.urls import path
from django.urls import include, re_path
from . import views
urlpatterns = [
    path('recommendation-request/', views.recommendation_request, name='recommendation_request'),
]