from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from accounts.serializers import UserSerializer
from accounts.models import User
from accounts.forms import RegisterUserForm
# Create your views here.

@api_view(['POST'])
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return Response({"message" : "user is registered"}, status=status.HTTP_201_CREATED)
    return Response({"message" : "user is not registered"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):

    return Response({"message" : "user is logged in"}, status=status.HTTP_202_ACCEPTED)