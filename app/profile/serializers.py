from rest_framework import serializers
from profile.models import Design, Map, FavoriteThing, LandingPage, Experience
from django.templatetags.static import static


class DesignSerializer(serializers.ModelSerializer):
    template_url = serializers.SerializerMethodField("get_static_template_url")
    example_url = serializers.SerializerMethodField("get_example_url")

    def get_static_template_url(self, design):
        return static(design.template_name)

    def get_example_url(self, design):
        return design.example.url

    class Meta:
        model = Design
        fields = ("id", "name", "template_url", "example_url")


class MapSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_static_url")

    def get_static_url(self, Map):
        return static(f"profile/assets/{Map.overlay_name}.svg")

    class Meta:
        model = Map
        fields = ("id", "location_name", "url")


class FavoriteThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteThing
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = "__all__"
