from accounts.models import Domain
from django.shortcuts import render

from .models import BlogPost


# Create your views here.
def blog_detail(request, slug):
    user = request.site.user

    blog_post = BlogPost.objects.get(slug=slug, author=user)

    context = {"meta": {"url": request.site.name, "name": str(user)}, "post": blog_post}

    return render(request, "blog/blog_detail.html", context)


def blog_index(request):
    user = request.site.user

    blogs = BlogPost.objects.filter(visibility="PU", author=user).order_by(
        "-created_date"
    )

    context = {"meta": {"url": request.site.name, "name": str(user)}, "posts": blogs}

    return render(request, "blog/blog_index.html", context)


def FilterBlogsByTags(request, tag):
    user = request.site.user

    blogs = BlogPost.objects.filter(tags__tag_name=tag, author=user)

    context = {
        "tag_name": tag,
        "posts": blogs,
        "meta": {"url": request.site.name, "name": str(user)},
    }

    return render(request, "blog/blog_tags.html", context)
