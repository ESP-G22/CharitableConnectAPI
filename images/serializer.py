from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['file']

class ImageUploadResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id']

class ImageRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['file']