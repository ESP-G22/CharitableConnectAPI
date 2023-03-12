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
        self.Test_event_create_er(token)

        self.Test_event_list(token)

        self.Test_event_get(token)
        self.Test_event_get_er(token)

        self.Test_event_update(token)
        self.Test_event_update_er(token)
        self.Test_event_update_er1(token)

        #self.Test_event_search(token)

        self.Test_event_delete_er1()
        self.Test_event_delete(token)
        self.Test_event_delete_er(token)
        
        

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
                "date": str(test_date),
                "address1": "45 Test Road",
                "postcode": "BA2 4AS", }
        response = self.client.post("/events/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.json()['msg'], 'New Event has been created')
        return
    
    # Create Event with no input data
    def Test_event_create_er(self, token):
        data = { "type": "", 
                "title": "", 
                "description": "", 
                "date": "",
                "address1": "",
                "postcode": "", }
        response = self.client.post("/events/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.json()['error'], 
                         {'type': ['A valid integer is required.'], 
                          'title': ['This field may not be blank.'], 
                          'description': ['This field may not be blank.'], 
                          'date': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return
    
    # Retrieve specified event
    def Test_event_get(self, token):
        response = self.client.get("/events/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
        return
    
    # Retrieve event that does not exist
    def Test_event_get_er(self, token):
        response = self.client.get("/events/0", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Event not found.')
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
        return
    
    # Update existing event with no input data
    def Test_event_update_er(self, token):
        data = { "type": "", 
                "title": "", 
                "description": "", 
                "date": "",
                "address1": "",
                "postcode": "", }
        response = self.client.put("/events/1", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], {'type': ['A valid integer is required.'], 
                                                    'title': ['This field may not be blank.'], 
                                                    'description': ['This field may not be blank.'], 
                                                    'date': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].']})
        return
    
    # Update non-existing event
    def Test_event_update_er1(self, token):
        data = { "type": "1", 
                "title": "Test_Event_Updated", 
                "description": "This event is going to be terrible!", 
                "date": str(test_date) }
        response = self.client.put("/events/0", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Event not found.')
        return

    # Search for a specific event
    def Test_event_search(self, token):
        data = { "searchTerm": "Test_Event_Updated", }
        response = self.client.get("/events/search", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return

    # Deletes a specified event
    def Test_event_delete(self, token):
        response = self.client.delete("/events/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['msg'], 'Event has been successfully deleted.')
        return
    
    # Deletes a non-existing event
    def Test_event_delete_er(self, token):
        response = self.client.delete("/events/0", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Event not found.')
        return
    
    # Attempts to delete an event but is unauthorized
    def Test_event_delete_er1(self):
        user = CCUser.objects.create_user(username='test_user2', email="test@test.com", password='very-strong-psw')
        login = {
            "username": "test_user2",
            "password": "very-strong-psw",
        }
        response = self.client.post("/user/login", login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()['token']
        response1 = self.client.delete("/events/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        return
  



