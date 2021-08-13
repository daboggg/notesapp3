from django import template
from main.models import *

register = template.Library()


@register.inclusion_tag('parts/sidebar.html', takes_context=True)
def sidebar_view(context):
    ctx = {
        'categories': NotesCategory.objects.all(),
    }

    if 'cat_selected' in context:
        ctx['cat_selected'] = context['cat_selected']
    else:
        ctx['cat_selected'] = ''
    return ctx