from django.contrib import admin

from .models import Design, Experience, LandingPage


# Register your models here.
class LandingPageAdmin(admin.ModelAdmin):
    pass


class ExperienceAdmin(admin.ModelAdmin):
    pass


class DesignAdmin(admin.ModelAdmin):
    pass


admin.site.register(LandingPage, LandingPageAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Design, DesignAdmin)
