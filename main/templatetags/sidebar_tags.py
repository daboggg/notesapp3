from django import template
from main.models import *

register = template.Library()


@register.inclusion_tag('parts/sidebar.html', takes_context=True)
def sidebar_view(context):
    return {
        'categories': NotesCategory.objects.all(),
        'cat_selected': context['cat_selected']
    }
