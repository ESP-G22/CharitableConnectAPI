from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from user.models import CCUser

class UserTestCase(APITestCase):

    # Allows for ordered execution of tests
    def test_order(self):

        # /user/register Endpoint Tests
        pk1, pk2 = self.Test_user_register()
        self.Test_user_register_same_username()
        self.Test_user_register_missing_username()
        self.Test_user_register_missing_password()
        self.Test_user_register_missing_email()

        # /user/login Endpoint Tests
        token = self.Test_user_login()
        self.Test_user_login_wrong_password()
        self.Test_user_login_invalid_username()
        self.Test_user_login_empty()

        # /user/list Endpoint Tests
        self.Test_user_list(token)
        self.Test_user_list_no_auth(token)

        # GET /user/profile Endpoint Tests
        self.Test_user_profile_get(token,pk1)
        self.Test_user_profile_get_no_auth(token,pk1)
        self.Test_user_profile_get_user_nonexistent(token,pk1)

        # PUT /user/profile Endpoint Tests
        self.Test_user_profile_update(token,pk1)
        self.Test_user_profile_update_no_auth(token,pk1)
        self.Test_user_profile_update_user_nonexistent(token,pk1)
        self.Test_user_profile_update_invalid_data(token,pk1)
        self.Test_user_profile_update_different_user(token,pk2)

        # /user/passwordchange Endpoint Tests
        self.Test_user_profile_passwordchange(token)
        self.Test_user_profile_passwordchange_no_auth(token)
        self.Test_user_profile_passwordchange_empty_data(token)
        self.Test_user_profile_passwordchange_wrong_password(token)

    # Register new user
    def Test_user_register(self):
        data1 = { "username": "test_user1",
                "email": "testUser1@mail.com",
                "password": "very-strong-psw"}
        data2 = { "username": "test_user2",
                "email": "testUser2@mail.com",
                "password": "very-strong-psw"}
        response1 = self.client.post("/user/register", data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.post("/user/register", data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        return int(response1.json()['pk']), int(response2.json()['pk'])
    
    # Register new user, but with an existing username
    def Test_user_register_same_username(self):
        data = { "username": "test_user1",
                "email": "testUser@mail.com",
                "password": "very-strong-psw"}
        response = self.client.post("/user/register", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    # Register new user, but with no username
    def Test_user_register_missing_username(self):
        data = { "email": "testUser@mail.com",
                "password": "very-strong-psw"}
        response = self.client.post("/user/register", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Register new user, but with no password
    def Test_user_register_missing_password(self):
        data = { "username": "test_user3",
                "email": "testUser@mail.com"}
        response = self.client.post("/user/register", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Register new user, but with no email
    def Test_user_register_missing_email(self):
        data = { "username": "test_user3",
                "password": "very-strong-psw"}
        response = self.client.post("/user/register", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Login as user
    def Test_user_login(self):
        data = { "username": "test_user1",
                "password": "very-strong-psw"}
        response = self.client.post("/user/login", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()['token']
    
    # Login as user, but with wrong password
    def Test_user_login_wrong_password(self):
        data = { "username": "test_user1",
                "password": "wrong-password"}
        response = self.client.post("/user/login", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Login as user, but with invalid username
    def Test_user_login_invalid_username(self):
        data = { "username": "test_user3",
                "password": "very-strong-psw"}
        response = self.client.post("/user/login", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Login as user, but with empty data
    def Test_user_login_empty(self):
        data = {}
        response = self.client.post("/user/login", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Lists all users
    def Test_user_list(self,token):
        response = self.client.get("/user/list", format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # Lists all users, but with no authentication
    def Test_user_list_no_auth(self,token):
        response = self.client.get("/user/list", format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    # Gets the profile of a user
    def Test_user_profile_get(self,token,pk):
        response = self.client.get(f"/user/profile/{pk}", format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # Gets the profile of a user, but with no authentication
    def Test_user_profile_get_no_auth(self,token,pk):
        response = self.client.get(f"/user/profile/{pk}", format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    # Gets the profile of a user, but with a user that doesn't exist
    def Test_user_profile_get_user_nonexistent(self,token,pk):
        response = self.client.get(f"/user/profile/3", format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    # Updates the profile of a user
    def Test_user_profile_update(self,token,pk):
        data = { "description": "This is a new description" }
        response = self.client.put(f"/user/profile/{pk}", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    # Updates the profile of a user, but with no authentication
    def Test_user_profile_update_no_auth(self,token,pk):
        data = { "description": "This is a new description" }
        response = self.client.put(f"/user/profile/{pk}", data, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    # Updates the profile of a user, but with a user that doesn't exist
    def Test_user_profile_update_user_nonexistent(self,token,pk):
        data = { "description": "This is a new description" }
        response = self.client.put(f"/user/profile/3", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    # Updates the profile of a user, but with invalid data
    def Test_user_profile_update_invalid_data(self,token,pk):
        data = { "random": "This is some random text" }
        response = self.client.put(f"/user/profile/{pk}", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    # Updates the profile of a user, but with a different, non-admin user
    def Test_user_profile_update_different_user(self,token,pk_other):
        data = { "description": "This is a new description" }
        response = self.client.put(f"/user/profile/{pk_other}", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    # Changes the password of a user
    def Test_user_profile_passwordchange(self,token):
        data = { "oldPassword": "very-strong-psw","newPassword":"even-stronger-psw"}
        response = self.client.put(f"/user/passwordchange", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    # Changes the password of a user, but with no authentication
    def Test_user_profile_passwordchange_no_auth(self,token):
        data = { "oldPassword": "very-strong-psw","newPassword":"even-stronger-psw"}
        response = self.client.put(f"/user/passwordchange", data, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    # Changes the password of a user, but with wrong old password
    def Test_user_profile_passwordchange_wrong_password(self,token):
        data = { "oldPassword": "incorrect-psw","newPassword":"even-stronger-psw"}
        response = self.client.put(f"/user/passwordchange", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    # Changes the password of a user, but with empty data
    def Test_user_profile_passwordchange_empty_data(self,token):
        data = {}
        response = self.client.put(f"/user/passwordchange", data, format='json',HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)



