from django.shortcuts import render

from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from .models import Movie
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated

## For API return Response
from rest_framework.response import Response
from rest_framework import status

## For Class base API views
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
# Create your views here.


class MovieView(APIView):
    def get(self, request):
        if (request.query_params.get('search') == None or request.query_params.get('search') == ""):
            movies = Movie.objects.all()
        else:
            movies = Movie.objects.filter(name__contains=request.query_params.get('search'))
        serilizer = MovieSerializer(movies, many=True)
        return Response(serilizer.data)


class DetailMovieView(APIView):
    def get_object(self, id):
        try: 
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk):
        serializer = MovieSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)


class WatchMarkAPI(APIView):
    serializer_class = WatchMarkSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data
            serializer = WatchMarkSerializer(data=data)

            if serializer.is_valid():
                watch = serializer.create(serializer.data, request.user)
                return Response({
                    'status': True,
                    'message': 'Movie added to watch/watched list'
                }, status=status.HTTP_201_CREATED)
            else:
                message = ''
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({
                    'status': False,
                    'message': message
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:
            data = request.data
            movie_obj = Movie.objects.get(id=request.data.get('movie'))
            action = request.data.get('action')
            is_update = Watch.objects.filter(user=request.user, movie=movie_obj).update(action=action)

            if is_update:
                return Response({
                    'status': True,
                    'message': 'Movie updated to watch/watched list.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'message': 'We are unable to update the request.'
                }, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):

        try:
            data = request.data
            movie_obj = Movie.objects.get(id=request.data.get('movie'))
            watch_obj = Watch.objects.get(user=request.user, movie=movie_obj)
            watch_obj.delete()

            return Response({
                'status': True,
                'message': 'Movie deleted from watch/watched list.'
            }, status=status.HTTP_200_OK)
        except Watch.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Requested movie does not exist in watch list.'
            }, status=status.HTTP_400_BAD_REQUEST)


class WatchListAPI(APIView):
    serializer_class = WatchListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            watch_obj = Watch.objects.filter(user=request.user, action="watch_list")
            watch_serializer = WatchListSerializer(watch_obj, many=True)
            movies = watch_serializer.data
            return Response({
                'status': True,
                'data': movies
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class WatchedListAPI(APIView):
    serializer_class = WatchedListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            watch_obj = Watch.objects.filter(user=request.user, action="watched_list")
            watch_serializer = WatchListSerializer(watch_obj, many=True)
            movies = watch_serializer.data
            return Response({
                'status': True,
                'data': movies
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)