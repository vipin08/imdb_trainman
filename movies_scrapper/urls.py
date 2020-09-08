from django.urls import path
from .views import ScrapperView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('api/v1/scrap/', ScrapperView.as_view()),
]
