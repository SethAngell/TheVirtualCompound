from django.urls import include, path
from accounts.views import api_create_custom_user

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("users/register-user/", api_create_custom_user),
]
