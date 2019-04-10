import hashlib
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def makehash(email):
    return hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()