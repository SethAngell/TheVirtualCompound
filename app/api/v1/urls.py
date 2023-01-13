from django.urls import include, path

from accounts.views import api_create_custom_user, api_get_registered_domain_mappings
from accounts.urls import api_urlpatterns

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("accounts/", include(api_urlpatterns)),
]
