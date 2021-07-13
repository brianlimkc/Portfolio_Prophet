from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from accounts.serializers import UserSerializer
from accounts.models import User
# Create your views here.

@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == "POST":
        new_user = UserSerializer(data=request.data)
        print(request.data)
        if new_user.is_valid():
            print("success")
            new_user.save()

    return Response({"message" : ""}, status=status.HTTP_201_CREATED)