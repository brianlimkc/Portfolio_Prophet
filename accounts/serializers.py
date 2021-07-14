from rest_framework import serializers
from accounts.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
            return User.objects.create_user(**validated_data)

