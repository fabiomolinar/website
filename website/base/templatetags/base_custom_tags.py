from django import template
from django.utils.translation import get_language
from django.template.defaultfilters import stringfilter

import re

"""Custom template tags"""

register = template.Library()

@register.filter
@stringfilter
def strip_lang(path):
    """Remove the language sub-directory from a given URL path
    
    >>> strip_lang('/pt/about/')
    '/about/'
    """
    pattern = '^(/%s)/' % get_language()
    match = re.search(pattern, path)
    if match is None:
        return path
    return path[match.end(1):]