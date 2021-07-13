from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from accounts.serializers import UserSerializer
from accounts.models import User
from accounts.forms import RegisterUserForm
# Create your views here.

@api_view(['GET', 'POST'])
def register_user(request):
    print(request.data)
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        print(form)
        if form.is_valid():
            print("success")
            form.save()

    return Response({"message" : "user is registered"}, status=status.HTTP_201_CREATED)