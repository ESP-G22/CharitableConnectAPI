from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

app_name = 'user'
urlpatterns = [
    #path('register/', CCUserRegisterEndpoint, name='register'),
    path('profile/', CCUserProfileView.as_view()),
    path('list/', ListUsersView.as_view()),
    path('gettoken', obtain_auth_token)
]