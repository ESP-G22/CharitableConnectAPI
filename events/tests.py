import datetime
import json
from django.test import TestCase
from django import forms

from django.contrib.auth.models import User
from django.test.client import Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from events.models import Event, Address
from events.serializers import *
from user.views import CCUserProfile


user = CCUser.objects.get(username='admin')
client = APIClient()
client.force_authenticate(user=user)

test_date = datetime.datetime(2023, 4, 15, 13, 43, 32, 10000)

class EventTestCase(APITestCase):

    def test_event_create(self):
        data = { "type": "0", 
                "title": "Test_Event", 
                "description": "This event is going to be fun!", 
                "date": str(test_date) }
        json_data = json.dumps(data, indent=4)
        response = client.post("/events/create", json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_view(self):
            response = client.get("/events/0")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
  



