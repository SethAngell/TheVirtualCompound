from django.urls import path

from blog.views import (
    blog_index,
    blog_detail,
    FilterBlogsByTags,
    api_get_create_update_delete_blog,
)

static_urlpatterns = [
    path("", blog_index, name="blog_index"),
    path("<slug:slug>", blog_detail, name="article_detail"),  # new
    path("topics/<str:tag>", FilterBlogsByTags, name="tags"),
]

api_urlpatterns = [
    path("", api_get_create_update_delete_blog.as_view()),
]
