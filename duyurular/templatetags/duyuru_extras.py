from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get a value from a dictionary by key"""
    return dictionary.get(key)

@register.filter
def get_attr(obj, attr_name):
    """Get an attribute from an object"""
    return getattr(obj, attr_name, None)