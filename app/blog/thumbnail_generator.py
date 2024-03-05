import imgkit
import os

TITLE_TOKEN = "[[BLOG TITLE]]"
SUBTITLE_TOKEN = "[[BLOG SUBTITLE]]"
NAME_TOKEN = "[[BLOG NAME]]"


def generate_html_string(title: str, subtitle: str, blog_name: str) -> str:
    app_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(app_dir, "templates/social_image.template.html")
    template = ""
    with open(template_path, "r") as ifile:
        template = ifile.read()
    return (
        template.replace(TITLE_TOKEN, title)
        .replace(SUBTITLE_TOKEN, subtitle)
        .replace(NAME_TOKEN, blog_name)
    )


def generate_screenshot(template_str: str):
    options = {"width": 1200, "height": 630}
    return imgkit.from_string(template_str, False, options=options)
