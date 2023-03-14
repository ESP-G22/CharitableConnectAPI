from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('upload', views.ImageUploadView.as_view()),
    path('<uuid:id>', views.ImageRetrieveView.as_view())
]