from rest_framework import serializers
from .models import CCUserProfile

class CCUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CCUserProfile
        fields = '__all__'