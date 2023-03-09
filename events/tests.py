import datetime
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.serializers import *
from user.models import CCUser
test_date = datetime.datetime(2023, 4, 15, 13, 43, 32, 10000)

class EventTestCase(APITestCase):
    def test_user_login(self):
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

    def test_event_create(self):
        pk, token = self.test_user_login()
        data = { "type": "0", 
                "title": "Test_Event", 
                "description": "This event is going to be fun!", 
                "date": str(test_date) }
        response = self.client.post("/events/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        # TODO: Test response JSON is in expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return
  



