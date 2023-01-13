from accounts.views import api_create_custom_user, api_get_registered_domain_mappings

from django.urls import path

api_urlpatterns = [
    path("register-user/", api_create_custom_user),
    path("all-domains/", api_get_registered_domain_mappings.as_view()),
]
