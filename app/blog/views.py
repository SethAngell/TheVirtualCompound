from blog.models import Blog, BlogPost, TopicTags, SocialImage
from blog.serializers import BlogPostSerializer, BlogSerializer, TopicTagSerializer
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# TODO: Grab SocialImage here
def blog_detail(request, slug):
    user = request.site.user

    blog_post = BlogPost.objects.get(slug=slug, parent_blog__blog_owner=user)
    social_image = SocialImage.objects.get(post=blog_post)

    context = {
        "meta": {"url": request.site.name, "name": str(user)},
        "post": blog_post,
        "social_image": social_image,
    }

    return render(request, "blog/blog_detail.html", context)


def blog_index(request):
    user = request.site.user

    blogs = BlogPost.objects.filter(
        visibility="PU", parent_blog__blog_owner=user
    ).order_by("-created_date")
    try:
        host = Blog.objects.get(blog_owner=user)
    except Blog.DoesNotExist:
        host = None

    context = {
        "meta": {"url": request.site.name, "name": str(user)},
        "posts": blogs,
        "blog": host,
    }

    return render(request, "blog/blog_index.html", context)


def FilterBlogsByTags(request, tag):
    user = request.site.user

    blogs = BlogPost.objects.filter(tags__tag_name=tag, parent_blog__blog_owner=user)

    context = {
        "tag_name": tag,
        "posts": blogs,
        "meta": {"url": request.site.name, "name": str(user)},
    }

    return render(request, "blog/blog_tags.html", context)


# API Views


class NoBlogExists(APIException):
    status_code = 404
    default_detail = "No blog configured for this user. Please create one."
    default_code = "Object does not exist"


class api_get_create_update_delete_blog(
    mixins.CreateModelMixin, RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(blog_owner=self.request.user)

    def get_object(self):
        if len(self.get_queryset()) > 0:
            return self.get_queryset()[0]
        else:
            raise NoBlogExists()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class api_list_create_blog_posts(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.filter(
            parent_blog__blog_owner=self.request.user
        ).order_by("created_date")


class api_retrieve_update_delete_blog_posts(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    permissions_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(parent_blog__blog_owner=self.request.user)


class api_list_create_topic_tags(ListCreateAPIView):
    serializer_class = TopicTagSerializer
    permissions_classes = [IsAuthenticated]
    queryset = TopicTags.objects.all()
