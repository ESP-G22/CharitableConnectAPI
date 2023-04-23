import datetime
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.serializers import *
from user.models import CCUser
test_date = datetime.datetime(2023, 4, 15, 13, 43, 32, 10000)

class RSVPTestCase(APITestCase):

    # Allows for ordered execution of tests
    def test_order(self):
        # SETUP
        pk, token = self.User_login() # ORGANISER
        pk1, token1 = self.User2_login() # USER
        self.Update_organiser(pk, token)

        # EVENT CREATE
        self.Test_event_create(token)

        # RSVP ADD
        self.Test_rsvps_add(token, token1)
        self.Test_rsvp_add_same_user(token)
        self.Test_rsvp_add_er(token)
        self.Test_rsvp_add_er1()

        # RSVP RETRIEVAL
        self.Test_rsvp_get(token)
        self.Test_rsvp_get_er(token)
        self.Test_rsvp_get_er1(token1)
        self.Test_rsvp_get_er2()

        # RSVP DELETION
        self.Test_rsvp_delete_er(token)
        self.Test_rsvp_delete_er1(token)
        self.Test_rsvp_delete(token)

        # RSVP DELETION ERRONEOUS
        self.Test_rsvp_delete_er2(token)
        self.Test_rsvp_delete_er3(token)
        self.Test_rsvp_delete_er4()

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
    
    # Creates another user for testing and logs the user in, returns primary key and token 
    def User2_login(self):
        user = CCUser.objects.create_user(username='test_user2', email="test@test.com", password='very-strong-psw')
        login = {
            "username": "test_user2",
            "password": "very-strong-psw",
        }
        response = self.client.post("/user/login", login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()['token']
        return user.pk, token
    
    # Creates another user for testing and logs the user in, returns primary key and token 
    def User3_login(self):
        user = CCUser.objects.create_user(username='test_user3', email="test@test.com", password='very-strong-psw')
        login = {
            "username": "test_user3",
            "password": "very-strong-psw",
        }
        response = self.client.post("/user/login", login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()['token']
        return user.pk, token
    
    # Updates a user to organiser status
    def Update_organiser(self, pk, token):
        data = { "userType": "ORGANISER", }
        response = self.client.put(f"/user/profile/{pk}", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['userType'], "ORGANISER")
        return

    """
    ---------------------------------------------
    
    EVENT TESTS

    ---------------------------------------------
    """

    """

    EVENT CREATION TESTS

    """

    # Creates multiple test Events
    def Test_event_create(self, token):
        data = { "type": "Other",
                "title": "Test_Event", 
                "description": "This event is going to be fun!", 
                "date": str(test_date),
                "address1": "45 Test Road",
                "postcode": "BA2 4AS", }
        data1 = { "type": "Other", 
                "title": "Test_Event1", 
                "description": "This event is going to be BAD!", 
                "date": str(test_date),
                "address1": "46 Test Road",
                "postcode": "BA2 4AB", }
        response = self.client.post("/events/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['msg'], 'New Event has been created')
        response1 = self.client.post("/events/create", data1, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json()['msg'], 'New Event has been created')
        return
    
    """
    ---------------------------------------------
    
    RSVP TESTS

    ---------------------------------------------

    """

    """
    
    RSVP CREATION TESTS

    """

    # Creates multiple rsvps for an event
    def Test_rsvps_add(self, token, token1):
        data = { "event": "1" }
        response = self.client.post("/rsvp/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        response1 = self.client.post("/rsvp/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token1}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['id'], 1)
        self.assertEqual(response1.json()['data']['id'], 2)
        return

    # Attempts to add rsvp for same user multiple times
    def Test_rsvp_add_same_user(self, token):
        data = { "event": "1" }
        response = self.client.post("/rsvp/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()['error'], 'RSVP has already been created.')
        return

    # Attemps to create an rsvp for an event that doesn't exist
    def Test_rsvp_add_er(self, token):
        data = { "event": "0" }
        response = self.client.post("/rsvp/create", data, format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Event does not exist.')
        return
    
    # Attempts to creates rsvp for an event without token
    def Test_rsvp_add_er1(self):
        data = { "event": "1" }
        response = self.client.post("/rsvp/create", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        return

    """
    
    RSVP RETRIEVAL TESTS

    """

    # Gets rsvp info
    def Test_rsvp_get(self, token):
        response = self.client.get("/rsvp/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['id'], 1)
        return

    # Attempts to get rsvp info of a non-existing event
    def Test_rsvp_get_er(self, token):
        response = self.client.get("/rsvp/0", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'RSVP does not exist.')
        return
    
    # Attemps to get rsvp info of a different user
    def Test_rsvp_get_er1(self, token1):
        response = self.client.get("/rsvp/1", format='json', HTTP_AUTHORIZATION=f'Token {token1}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['error'], 'Unauthorized. This RSVP does not belong to current user.')
        return

    # Attempts to get rsvp info without a token
    def Test_rsvp_get_er2(self):
        response = self.client.get("/rsvp/1", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        return

    """
    
    RSVP DELETION TESTS

    """

    # Attempts to delete an rsvp that doesn't exist
    def Test_rsvp_delete_er(self, token):
        response = self.client.delete("/rsvp/0", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'RSVP does not exist.')
        return

    # Attempts to delete an rsvp that doesn't belong to the user
    def Test_rsvp_delete_er1(self, token):
        response = self.client.delete("/rsvp/2", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['error'], 'Unauthorized. This RSVP does not belong to current user.')
        return

    # Deletes the rsvp for an event
    def Test_rsvp_delete(self, token):
        response = self.client.delete("/rsvp/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['msg'], 'RSVP has been deleted.')
        return
    
    # Attemps to get an rsvp for an event that has been deleted
    def Test_rsvp_delete_er2(self, token):
        response = self.client.get("/rsvp/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'RSVP does not exist.')
        return

    # Attempts to delete an rsvp for an event that has been deleted
    def Test_rsvp_delete_er3(self, token):
        response = self.client.delete("/rsvp/1", format='json', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'RSVP does not exist.')
        return
    
    # Attempts to delete an rsvp without a token
    def Test_rsvp_delete_er4(self):
        response = self.client.delete("/rsvp/2", format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        return