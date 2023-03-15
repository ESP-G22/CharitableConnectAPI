from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.CCRSVPView.as_view()),
    path('create', views.CCRSVPCreationView.as_view()),
    path('subscribed', views.CCRSVPUserListView.as_view())
]