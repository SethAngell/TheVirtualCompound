from django.urls import include, path

from accounts.urls import api_urlpatterns as accounts_urls
from profile.urls import api_urlpatterns as profile_urls
from content.urls import api_urlpatterns as content_urls
from blog.urls import api_urlpatterns as blog_urls

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("accounts/", include(accounts_urls)),
    path("profiles/", include(profile_urls)),
    path("content/", include(content_urls)),
    path("blog/", include(blog_urls)),
]
