from django import template
register = template.Library()

def get(d, key):
    return d.get(key, '')

register.filter(get)