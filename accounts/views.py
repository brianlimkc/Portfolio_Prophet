from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User
from accounts.forms import RegisterUserForm

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == "POST":
        print(request.data)
        print(request.POST)
        form = RegisterUserForm(request.data)

        if form.is_valid():
            form.save()
            return Response({"message" : "user is registered"}, status=status.HTTP_201_CREATED)
        else:
            print(form.errors)
            return Response({"message" : "check input for user"}, status=status.HTTP_400_BAD_REQUEST)
#     return Response({"message" : "user is registered"}, status=status.HTTP_201_CREATED)
    return Response({"message" : "user is not registered"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_login(request):

    return Response({"message" : "user is logged in"}, status=status.HTTP_200_OK)
