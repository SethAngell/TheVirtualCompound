from rest_framework import serializers
from blog.models import BlogPost, Blog, TopicTags


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class TopicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTags
        fields = "__all__"
