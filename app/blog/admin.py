from django.contrib import admin

from .models import Blog, BlogPost, PostImage, TopicTags, SocialImage


# Register your models here.
class PostImageAdmin(admin.ModelAdmin):
    pass


class BlogPostAdmin(admin.ModelAdmin):
    pass


class TopicTagAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    pass


class SocialImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(PostImage, PostImageAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(TopicTags, TopicTagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(SocialImage, SocialImageAdmin)
