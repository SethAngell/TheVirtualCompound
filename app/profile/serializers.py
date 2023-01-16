from rest_framework import serializers
from profile.models import Design, Map, FavoriteThing, LandingPage, Experience
from django.templatetags.static import static


class DesignSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_static_url")

    def get_static_url(self, design):
        return static(design.template_name)

    class Meta:
        model = Design
        fields = ("id", "name", "url")


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
