from django.urls import path

from . import views

urlpatterns = [
    path("new_invite/", views.create_new_invite, name="new_user_invitation"),
]
