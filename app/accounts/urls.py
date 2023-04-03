from accounts.views import (
    api_create_custom_user,
    api_get_registered_domain_mappings,
    api_get_current_user_info,
)

from django.urls import path

api_urlpatterns = [
    path("user/", api_create_custom_user),
    path("domains/", api_get_registered_domain_mappings.as_view()),
    path("user/info/", api_get_current_user_info),
]

static_url_patterns = []
