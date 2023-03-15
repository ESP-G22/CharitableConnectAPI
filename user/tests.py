from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from user.models import CCUser

class UserTestCase(APITestCase):

    # Allows for ordered execution of tests
    def test_order(self):
        pk = self.Test_user_register()
        token = self.Test_user_login()
        self.Test_user_list(token)
        self.Test_user_profile_get(token,pk)
        self.Test_user_profile_update(token,pk)
        self.Test_user_profile_passwordchange(token)

    # Register new user
    def Test_user_register(self):
        data = { "username": "test_user1",
                "email": "testUser@mail.com",
                "password": "very-strong-psw"}
        response = self.client.post("/user/register", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return int(response.json()['pk'])
    
    # Login as user
    def Test_user_login(self):
        data = { "username": "test_user1",
                "password": "very-strong-psw"}
        response = self.client.post("/user/login", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()['token']
    
    # Lists all users
    def Test_user_list(self,token):
        response = self.client.get("/user/list", format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # Gets the profile of a user
    def Test_user_profile_get(self,token,pk):
        response = self.client.get(f"/user/profile/{pk}", format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # Updates the profile of a user
    def Test_user_profile_update(self,token,pk):
        data = { "description": "This is a new description" }
        response = self.client.put(f"/user/profile/{pk}", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # Changes the password of a user
    def Test_user_profile_passwordchange(self,token):
        data = { "oldPassword": "very-strong-psw","newPassword":"even-stronger-psw"}
        response = self.client.put(f"/user/passwordchange", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)



