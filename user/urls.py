from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('login', obtain_auth_token),
    path('profile/<int:pk>', CCUserProfileView.as_view()),
    path('list', CCUserListView().as_view()),
    path('register', CCUserRegisterView.as_view()),
    path('passwordchange', CCUserPasswordChangeView.as_view()),
    path('follow/<int:pk>', CCUserFollowView.as_view())
]

#urlpatterns += router.urls