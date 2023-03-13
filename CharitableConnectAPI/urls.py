"""CharitableConnectAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Gets the schema view for the documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Charitable Connect API",
        default_version='v1',
        description="The Django API for the Charitable Connect application",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    #url="https://api.cc.n0ne1eft.dev/",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('events/', include('events.urls')),
    path('rsvp/', include('rsvp.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
