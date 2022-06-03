from django import template

register = template.Library()


@register.filter
def return_item(t_dictionary, i):
    try:
        return t_dictionary[int(i)]
    except:  # noqa: E722
        return None
