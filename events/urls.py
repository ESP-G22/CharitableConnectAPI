from django.urls import path 
from . import views

urlpatterns = [
    path('<int:pk>', views.CCEventView.as_view()),
    path('list', views.CCEventListView.as_view()),
    path('create', views.CCEventCreationView.as_view()),
    path('search', views.CCEventSearchView.as_view()),
]