import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    pattern = ''
    try:
        pattern = '^.*$' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
    
# from django import template
# register = template.Library()
#
# @register.simple_tag
# def active(request, pattern):
#     import re
#     if re.search(pattern, request.path):
#         return 'active'
#     return ''
# <li class="{% if request.resolver_match.url_name == "my_view_name" %}active{% endif %}"><a href="{% url "my_view_name" %}">Shortcut1</a></li>
