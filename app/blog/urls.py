from django.urls import path

from blog.views import (
    blog_index,
    blog_detail,
    FilterBlogsByTags,
    api_get_create_update_delete_blog,
    api_list_create_blog_posts,
    api_retrieve_update_delete_blog_posts,
    api_list_create_topic_tags,
)

static_urlpatterns = [
    path("", blog_index, name="blog_index"),
    path("<slug:slug>", blog_detail, name="article_detail"),  # new
    path("topics/<str:tag>", FilterBlogsByTags, name="tags"),
]

api_urlpatterns = [
    path("", api_get_create_update_delete_blog.as_view()),
    path("post/<int:pk>/", api_retrieve_update_delete_blog_posts.as_view()),
    path("posts/", api_list_create_blog_posts.as_view()),
    path("tags/", api_list_create_topic_tags.as_view()),
]
