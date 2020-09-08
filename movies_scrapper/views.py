from django.shortcuts import render

from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

## For API return Response
from rest_framework.response import Response
from rest_framework import status

## For Class base API views
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
# Create your views here.
from .tasks import scrapping_from_url
from celery import shared_task

@authentication_classes([])
@permission_classes([])
class ScrapperView(APIView):
    def post(self, request):
        if request.data.get('url') == None or request.data.get('url') == "": 
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        data = scrapping_from_url.delay(request.data.get('url'))
        return Response(status=status.HTTP_200_OK)
