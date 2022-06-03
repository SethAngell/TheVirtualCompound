import xml.etree.cElementTree as et

from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils.html import mark_safe


# Validators
def is_svg(file):
    tag = None
    try:
        for event, el in et.iterparse(file, ("start",)):
            tag = el.tag
            break
    except et.ParseError:
        pass
    return tag == "{http://www.w3.org/2000/svg}svg"


def validate_svg(file):
    if not is_svg(file.file):
        raise ValidationError("File not svg")


# Models
class Design(models.Model):
    template_name = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Map(models.Model):
    location_name = models.CharField(max_length=150)
    overlay_name = models.CharField(max_length=150)

    def __str__(self):
        return self.location_name


# TODO: Add a better way to extract values from SVG for more dynamic use
#   -> Pull Path and Viewbox
#   -> Reconstruct SVG in template with Tailwind classes for colors
class FavoriteThing(models.Model):
    thing_name = models.CharField(max_length=150)
    svg_icon = models.FileField(upload_to="favorite_things/")
    path_attribute = models.CharField(max_length=10000, null=True, blank=True)
    viewbox_attribute = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"Icon: {self.thing_name}"

    def image_tag(self):
        return mark_safe(
            f'<img src="{settings.MEDIA_URL}/%s" width="150" height="150" />'
            % (self.svg_icon)
        )

    image_tag.short_description = "Image"

    def extract_path(self, file):
        tree = et.parse(file)
        root = tree.getroot()

        viewbox = root.attrib["viewBox"]
        path = tree.find("./path").attrib["d"]
        print(len(path), path[:10], len(viewbox), viewbox[:10])

        return path, viewbox

    def save(self, *args, **kwargs):
        self.path_attribute, self.viewbox_attribute = self.extract_path(
            self.svg_icon.file.file
        )
        super(FavoriteThing, self).save(*args, **kwargs)


class LandingPage(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    bio = models.TextField()
    headline = models.CharField(max_length=100)
    avatar = models.ImageField()

    contact_email = models.EmailField(null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    spotify = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(null=True, blank=True)
    favorite_things = models.ManyToManyField(FavoriteThing, blank=True)
    map_overlay = models.ForeignKey(
        Map, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    template = models.ForeignKey(
        Design, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exp_id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=40)
    title = models.CharField(max_length=65)
    description = models.TextField(blank=True, null=True)
    present = models.BooleanField()
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.company
