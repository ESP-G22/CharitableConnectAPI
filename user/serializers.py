from rest_framework import serializers
from .models import *

class CCUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CCUserProfile
        fields = '__all__'

class CCUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCUser
        fields = ['username','email','pk']

class CCUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCUser
        fields = ['username', 'email', 'password']