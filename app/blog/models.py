import os
import re
import tempfile
from ast import Bytes
from io import BytesIO

import markdown
from accounts.models import CustomUser
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from PIL import Image, UnidentifiedImageError


class Blog(models.Model):
    blog_name = models.CharField(max_length=256)
    blog_description = models.CharField(max_length=512, blank=True, null=False)
    blog_owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog_name

    def save(self, *args, **kwargs):
        if len(self.blog_description) == 0:
            self.blog_description = f"{self.blog_owner}'s Blog"

        super().save(*args, **kwargs)


class TopicTags(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name


class PostImage(models.Model):
    reference = models.CharField(max_length=128)
    alt_text = models.TextField(blank=False)
    image = models.ImageField(upload_to="blog_images")
    thumbnail = models.ImageField(
        upload_to="blog_images/thumbnails", editable=False, blank=True, null=True
    )

    def __str__(self):
        return self.reference

    # https://stackoverflow.com/a/23927211
    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail((1200, 630), Image.LANCZOS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + "_thumb" + thumb_extension

        if thumb_extension in [".jpg", ".jpeg"]:
            FTYPE = "JPEG"
        elif thumb_extension == ".gif":
            FTYPE = "GIF"
        elif thumb_extension == ".png":
            FTYPE = "PNG"
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def generate_png_version(self, p_image, p_name):
        """
        Generates new DjangoFile object containing the converted and renamed image
        Note: Image is renamed after the reference var
        """
        # Adapted from https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/
        g_image = Image.open(p_image)
        g_io = BytesIO()  # create a BytesIO object
        g_image.save(g_io, "PNG")  # save image to BytesIO object
        generated_image = File(
            g_io, name=f"{p_name}.png"
        )  # create a django friendly File object

        return generated_image

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.generate_png_version(self.image, self.reference)

        if not self.make_thumbnail():
            raise Exception("Could not create thumbnail - is the file type valid?")

        super().save(*args, **kwargs)


class BlogPost(models.Model):

    title = models.CharField(max_length=256, blank=True)
    markdown_body = models.TextField()
    html_body = models.TextField(blank=True)
    tags = models.ManyToManyField(TopicTags)
    preview = models.CharField(max_length=400, blank=True)
    slug = models.SlugField(null=False, unique=True, blank=True, max_length=256)
    created_date = models.DateField(auto_now_add=True, blank=True)
    updated = models.DateField(auto_now=True, blank=True)
    visibility = models.CharField(
        max_length=2, choices=[("PU", "Public"), ("PR", "Private")]
    )
    parent_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=False)

    open_graph_protocol_description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

    def extension(self):
        name, extension = os.path.splitext(self.header_image.thumbnail.url)
        return extension

    def determine_image_encoding(self):
        if self.extension().lower() in ["jpg", "jpeg"]:
            return "image/jpeg"
        else:
            return "image/png"

    def pretty_preview(self):

        size_bins = [350, 300, 250, 200, 150, 100, 50]
        bin_index = 0

        words = self.extract_title()[1].split(" ")
        preview_extracted = False

        while preview_extracted is False:
            preview = ""

            while (len(preview) < size_bins[bin_index]) and (len(words) > 0):
                preview += words.pop(0)
                preview += " "

            preview = preview[:-1]
            preview += "..."

            markdown_preview = markdown.markdown(preview)

            if len(markdown_preview) <= 400:
                return markdown_preview
            else:
                bin_index += 1

    def extract_title(self):
        split_text = self.markdown_body.split("\n")
        title = split_text[0]
        title = title[2:]

        titleless_body = "\n".join(split_text[1:])

        return (title, titleless_body)

    def classify_components(self):
        mappings = [
            (r"(<h2)(>(.*?)</h2>)", '\g<1> class="text-2xl font-bold mt-2 pb-1"\g<2>'),
            (r"(<h3)(>(.*?)</h3>)", '\g<1> class="text-xl font-bold mt-2 pb-1"\g<2>'),
            (r"(<h4)(>(.*?)</h4>)", '\g<1> class="font-bold mt-2 pb-1"\g<2>'),
            (r"(<p)(>(.*?)</p>)", '\g<1> class="pb-3"\g<2>'),
            (r"(<ul)(>(.*?)</ul>)", '\g<1> class="list-disc pl-16 pb-1"\g<2>'),
            (r"(<ol)(>(.*?)</ol>)", '\g<1> class="list-decimal pl-16 pb-1"\g<2>'),
            (
                r"(<pre)(>(.*?)</pre>)",
                '\g<1> class="my-3 pb-3 px-3 py-4 w-full bg-slate-800 text-slate-50 dark:bg-slate-600 rounded-lg" \g<2>',
            ),
            (
                r"(<p class=\"pb-3)(\"><code>(.*?)</code></p>)",
                "\g<1> my-3 pb-3 px-3 py-4 w-full bg-slate-800 text-slate-50 dark:bg-slate-600 rounded-lg\g<2>",
            ),
        ]

        for mapping in mappings:
            self.html_body = re.sub(mapping[0], mapping[1], self.html_body, flags=re.S)

    def save(self, *args, **kwargs):  # new
        title, body = self.extract_title()
        self.title = title
        if len(self.preview) == 0:
            self.preview = self.pretty_preview()
        self.open_graph_protocol_description = "".join(
            BeautifulSoup(self.preview).findAll(text=True)
        )
        self.image_encoding = self.determine_image_encoding()
        self.html_body = markdown.markdown(
            self.markdown_body,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.footnotes",
            ],
        )
        # self.classify_components()

        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class SocialImage(models.Model):
    ENCODING_TYPE = "png"

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        blank=True, null=False, upload_to="blog_images/social_images"
    )

    def _generate_hero_image():
        # do stuff
        return None

    def save(self, *args, **kwargs):
        self.image = self._generate_hero_image()

        return super().save(*args, **kwargs)


@receiver(post_save, sender=BlogPost)
def my_handler(sender, **kwargs):
    new_social_image = SocialImage(post=sender)
    new_social_image.save()
