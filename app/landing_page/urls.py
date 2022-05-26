from django.urls import path

from . import views

urlpatterns = [path("", views.LandingPageView, name="home")]
