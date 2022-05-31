from re import A

from django.contrib import admin

from .models import Design, Experience, FavoriteThing, LandingPage


# Register your models here.
class LandingPageAdmin(admin.ModelAdmin):
    pass


class ExperienceAdmin(admin.ModelAdmin):
    pass


class DesignAdmin(admin.ModelAdmin):
    pass


class FavoriteThingAdmin(admin.ModelAdmin):
    fields = ["svg_icon", "thing_name", "image_tag"]
    readonly_fields = ["image_tag"]


admin.site.register(LandingPage, LandingPageAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Design, DesignAdmin)
admin.site.register(FavoriteThing, FavoriteThingAdmin)
