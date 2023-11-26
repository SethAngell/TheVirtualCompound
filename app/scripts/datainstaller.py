import os
import json
from profile.models import FavoriteThing, Map, Design
from profile.serializers import ExperienceSerializer
from django.core.files import File


def loadConfig():
    with open("/usr/src/app/scripts/config.json") as json_file:
        return json.load(json_file)


def loadFavoriteThings(config):
    custom_icons = [
        icon for icon in os.listdir(config["STATIC"]["FAVORITE_THINGS_SVG_DIRECTORY"])
    ]
    existing_favorite_things = FavoriteThing.objects.all()
    fresh_start = len(existing_favorite_things) == 0

    if fresh_start:
        for icon in custom_icons:
            full_path = f'{config["STATIC"]["FAVORITE_THINGS_SVG_DIRECTORY"]}/{icon}'
            with open(full_path, "r") as ifile:
                django_file = File(ifile, icon)
                new_icon = FavoriteThing(svg_icon=django_file)
                new_icon.save()


def loadMaps(config):
    for city_name, city_path in config["Maps"].items():
        newMap = Map(location_name=city_name, overlay_name=f"{city_path}_overlay")
        newMap.save()


def loadDesigns(config):
    for design in config["Templates"]:
        with open(design["example"], "rb") as ifile:
            django_file = File(ifile, design["example"].split("/")[-1])
            newTemplate = Design(
                template_name=design["template_name"],
                name=design["name"],
                example=django_file,
            )
            newTemplate.save()


def loadExperiences(config):
    for experience in config["Experiences"]:
        newExp = ExperienceSerializer(data=experience)
        newExp.is_valid()
        newExp.save()


def run():
    config = loadConfig()
    loadFavoriteThings(config)
    loadMaps(config)
    loadDesigns(config)
    loadExperiences(config)
