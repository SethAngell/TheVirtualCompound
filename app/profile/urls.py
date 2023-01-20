from django.urls import path

from profile.views import (
    LandingPageView,
    api_get_available_designs,
    api_get_available_maps,
    api_get_available_favorite_things,
    api_get_update_delete_experience,
    api_create_experience,
    api_get_update_delete_landing_page,
    api_create_landing_page,
)

static_urlpatterns = [path("", LandingPageView, name="home")]

api_urlpatterns = [
    path("designs/", api_get_available_designs.as_view()),
    path("maps/", api_get_available_maps.as_view()),
    path("favorite-things/", api_get_available_favorite_things.as_view()),
    path("experience/", api_create_experience.as_view()),
    path("experience/<int:pk>/", api_get_update_delete_experience.as_view()),
    path("landing-page/", api_create_landing_page.as_view()),
    path("landing-page/<int:pk>/", api_get_update_delete_landing_page.as_view()),
]
