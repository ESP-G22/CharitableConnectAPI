import datetime
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.serializers import *
from user.models import CCUser
test_date = datetime.datetime(2023, 4, 15, 13, 43, 32, 10000)

class EventTestCase(APITestCase):

    # Allows for ordered execution of tests
    def test_order(self):
        pk, token = self.User_login()
        self.Test_event_create(token)
        self.Test_event_list(token)
        self.Test_event_get(token)
        self.Test_event_update(token)
        self.Test_event_search(token)

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
    
    # Create Event
    def Test_event_create(self, token):
        data = { "type": "0", 
                "title": "Test_Event", 
                "description": "This event is going to be fun!", 
                "date": str(test_date) }
        response = self.client.post("/events/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.json()['msg'], 'New Event has been created')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return
    
    # Retrieve specified event
    def Test_event_get(self, token):
        response = self.client.get("/events/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
        return

    # List all events
    def Test_event_list(self, token):
        response = self.client.get("/events/list", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return
    
    # Update existing event
    def Test_event_update(self, token):
        data = { "type": "1", 
                "title": "Test_Event_Updated", 
                "description": "This event is going to be terrible!", 
                "date": str(test_date) }
        response = self.client.put("/events/1", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['msg'], 'Event has been successfully updated.')

    # Search for a specific event
    def Test_event_search(self, token):
        data = { "searchTerm": "Test_Event_Updated", }
        response = self.client.get("/events/search", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


  



