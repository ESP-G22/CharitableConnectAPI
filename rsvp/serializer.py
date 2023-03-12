from rest_framework import serializers
from .models import *

class CCRSVPCreationSerializer(serializers.Serializer):
    event = serializers.IntegerField(required=True)

class CCRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'