from django.urls import path

from content.views import (
    api_list_create_user_documents,
    api_get_update_delete_user_document,
    api_list_create_user_images,
    api_get_update_delete_user_image,
)

api_urlpatterns = [
    path("image/", api_list_create_user_images.as_view()),
    path("image/<int:pk>/", api_get_update_delete_user_image.as_view()),
    path("document/", api_list_create_user_documents.as_view()),
    path("document/<int:pk>/", api_get_update_delete_user_document.as_view()),
]
