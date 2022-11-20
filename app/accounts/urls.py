from django.urls import path

from . import views

urlpatterns = [
    path("new_invite/", views.create_new_invite, name="new_user_invitation"),
    path("accept_invite/", views.validate_invited_user, name="accept_invitation"),
]
