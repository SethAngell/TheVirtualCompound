from django.urls import path

from profile.views import (
    LandingPageView,
    api_get_available_designs,
    api_get_available_maps,
    api_get_available_favorite_things,
)

static_urlpatterns = [path("", LandingPageView, name="home")]

api_urlpatterns = [
    path("designs/", api_get_available_designs.as_view()),
    path("maps/", api_get_available_maps.as_view()),
    path("favorite-things/", api_get_available_favorite_things.as_view()),
]
