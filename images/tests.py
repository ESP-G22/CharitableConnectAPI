import datetime
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.serializers import *
from user.models import CCUser
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image

class ImageTestCase(APITestCase):

    def test_order(self):
        temp = SimpleUploadedFile(name='test_image.jpg', content=open('images/testImages/test_image.jpg', 'rb').read(), content_type='image/jpeg')
        pk, token = self.User_login()
        self.Test_Image_Upload(token, temp)
        return
    
    """
    ---------------------------------------------
    
    SETUP FUNCTIONS FOR USERS TO BE USED IN TESTS

    ---------------------------------------------
    """

    # Creates a user for testing and logs the user in, returns primary key and token    
    def User_login(self):
        """
        Copied from User Tests, create a test user and return pk and token
        """
        user = CCUser.objects.create_user(username='test_user1', email="test@test.com", password='very-strong-psw')
        login = {
            "username": "test_user1",
            "password": "very-strong-psw",
        }
        response = self.client.post("/user/login", login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return user.pk, response.json()['token']
    
    # Uploads an image, returning UUID
    def Test_Image_Upload(self, token, testPhoto):
        data = { "file": testPhoto, }
        response = self.client.post("/images/upload", data, format='multipart', HTTP_AUTHORIZATION=f'Token {token}')
        print(response.json())
        print(response.status_code)
        return