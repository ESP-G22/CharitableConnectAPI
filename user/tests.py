import datetime
import json
from django.test import TestCase
from django import forms

from django.contrib.auth.models import User
from django.test.client import Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from user.views import *
from user.models import *

class UserTestCase(APITestCase):

    client = APIClient()
    #client.force_authenticate(user=CCUser.objects.get(username='admin'))

    # Register new user
    def test_user_register(self):
        data = { "username": "test_user1", 
                "email": "testUser@mail.com", 
                "password": "very-strong-psw"}
        json_data = json.dumps(data, indent=4)
        response = self.client.post("/user/register", json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_view_profile(self):
        response = self.client.get("/user/profile/1", content_type="application/json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)




