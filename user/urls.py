from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('login/', obtain_auth_token),
    path('user/<int:pk>', CCUserProfileView.as_view())
]

#urlpatterns += router.urls