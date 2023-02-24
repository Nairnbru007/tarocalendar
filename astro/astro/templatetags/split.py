
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter(name='split')
#@register.filter(needs_autoescape=True)
def split(value, key):
  return value.split(key)
