from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.serializers import *
from user.models import CCUser
from django.core.files.uploadedfile import SimpleUploadedFile

class ImageTestCase(APITestCase):

    # Allows for ordered execution of tests
    def test_order(self):
        # SETUP
        FAKEUUID = "37cbb78c-f044-49d7-9f33-39a9365dd8ff"
        temp = SimpleUploadedFile(name='test_image.jpg', content=open('images/testImages/test_image.jpg', 'rb').read(), content_type='image/jpeg')
        temp1 = SimpleUploadedFile(name='test_image1.jpg', content="", content_type='image/jpeg')
        pk, token = self.User_login()

        # IMAGE UPLOAD
        UUID = self.Test_image_upload(token, temp)
        self.Test_image_upload_er(token, temp)
        self.Test_image_upload_er1(token, temp1)
        self.Test_image_upload_er2(temp1)

        # IMAGE DOWNLOAD
        self.Test_image_download(token, UUID)
        self.Test_image_download_er(token, FAKEUUID)

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
    
    """
    ---------------------------------------------
    
    Image Tests

    ---------------------------------------------
    """

    """

    IMAGE UPLOAD TESTS

    """

    # Uploads an image, returning UUID
    def Test_image_upload(self, token, testPhoto):
        data = { "file": testPhoto, }
        response = self.client.post("/images/upload", data, format='multipart', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(response.json()['id'], ".{8}-.{4}-.{4}-.{4}-.{12}")
        return response.json()['id']
    
    # Attempts to upload the original image after it has already been uploaded
    def Test_image_upload_er(self, token, testPhoto):
        data = { "file": testPhoto, }
        response = self.client.post("/images/upload", data, format='multipart', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.json()['file'][0], 'The submitted file is empty.')
        return
    
    # Attempts to upload an empty file
    def Test_image_upload_er1(self, token, testPhoto):
        data = { "file": testPhoto, }
        response = self.client.post("/images/upload", data, format='multipart', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.json()['file'][0], 'The submitted file is empty.')
        return

    # Attempts to upload an image without token
    def Test_image_upload_er2(self, testPhoto):
        data = { "file": testPhoto, }
        response = self.client.post("/images/upload", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertRegex(response.json()['detail'], 'Authentication credentials were not provided.')
        return
    
    """

    IMAGE DOWNLOAD TESTS

    """

    # Downloads an image based off image ID
    def Test_image_download(self, token, uuid):
        response = self.client.get(f"/images/{uuid}", HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # NOT SURE HOW TO IMPLEMENT A CHECK FOR A RETURNED IMAGE
        return
    
    # Attempts to download an image with an invalid ID
    def Test_image_download_er(self, token, uuid):
        response = self.client.get(f"/images/{uuid}", HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Image not found')
        return