from django.urls import path
from .views import MovieView, DetailMovieView, WatchMarkAPI, WatchListAPI, WatchedListAPI
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('api/v1/movie/', MovieView.as_view(), name='movie-list-api'),
    path('api/v1/movie/<int:pk>', DetailMovieView.as_view(), name='movie-details-api'),
    path('api/v1/watch_or_watched', WatchMarkAPI.as_view(), name='watch-mark-api'),
    path('api/v1/my_watch_list/', WatchListAPI.as_view(), name='movie-get-all-watch-list'),
    path('api/v1/my_watched_list/', WatchedListAPI.as_view(), name='movie-get-all-watched-list'),
]
