from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
# Create your views here.

@api_view(['GET'])
def register_user(request):
    

    return Response({"message" : "route hit"}, status=status.HTTP_201_CREATED)