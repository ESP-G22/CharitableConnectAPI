from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from user.models import CCUser

class UserTestCase(APITestCase):

    # Register new user
    def test_user_register(self):
        data = { "username": "test_user1",
                "email": "testUser@mail.com",
                "password": "very-strong-psw"}
        response = self.client.post("/user/register", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login(self):
        # Create User in Database, alternatively call test_user_register above
        user = CCUser.objects.create_user(username='test_user1', email="test@test.com", password='very-strong-psw')
        login = {
            "username": "test_user1",
            "password": "very-strong-psw",
        }
        response = self.client.post("/user/login", login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return user.pk, response.json()['token'] # Return user pk and token

    def test_user_view_profile(self):
        pk, token = self.test_user_login()
        response = self.client.get(f"/user/profile/{pk}", HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: AssertEqual JSON Response




