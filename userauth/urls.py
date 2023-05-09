"""
URL configuration for userauth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from myapp.views import UserCreateView, LoginAPIView, UserLogoutAPIView, UserViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers


# this is coming from drf_yasg, it is used to Document all the APIs in our project at swagger/ or at redoc/ (line no. 47,48)
schema_view = get_schema_view (
    openapi.Info(
        title="My APIs",
        default_version='v1',
        description="Your API description",
        terms_of_service="",
        contact=openapi.Contact(email="ashishkush1122@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# Payload

# REGISTER
"""
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123",
    "date_of_birth": "1990-01-01",
    "mobile_number": "1234567890",
    "address": "123 Main St",
    "pancard_number": "ABCDE1234F"
}

"""

# LOGIN
""" 
{
    "email": "john.doe@example.com",
    "password": "password123"
}

"""

# LOGOUT
"""
In the Header add key:value
Authorization : Token token_obtained_when_logged_in
"""