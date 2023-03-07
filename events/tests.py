import datetime
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from events.models import Event, Address
from events.serializers import *
from user.models import CCUser



class CreateEventTestCase(APITestCase):

    # Test to create user and store token for event tests.

    def test_create(self):
        data = {"type": 1, "title": "Test_Event",
                "description": "This event is going to be fun!",
                "date": datetime.date.fromisocalendar(2023, 42, 3)}
        response = self.client.post("/events/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EventViewTestCase(APITestCase):
    def test_view(self):
        response = self.client.get("/events/0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

