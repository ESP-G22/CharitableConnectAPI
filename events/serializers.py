from rest_framework import serializers
from .models import *
from user.serializers import CCUserProfileSerializer
class CCEventSerializer(serializers.ModelSerializer):
    organiser = CCUserProfileSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class CCNewEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['organiser']

class CCEventSearchSerializer(serializers.Serializer):
    searchTerm = serializers.CharField()
