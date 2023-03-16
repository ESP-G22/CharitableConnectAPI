from rest_framework import serializers
from .models import *

class CCUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    followerCount = serializers.IntegerField(read_only=True)
    eventCount = serializers.IntegerField(read_only=True)
    class Meta:
        model = CCUserProfile
        fields = '__all__'

class CCUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCUser
        fields = ['username','email','pk']

class CCUserRegisterSerializer(serializers.Serializer):
    model = CCUser
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class CCUserPasswordChangeSerializer(serializers.Serializer):
    model = CCUser
    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
