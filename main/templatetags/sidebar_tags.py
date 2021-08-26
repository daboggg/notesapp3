from django import template
from django.db.models import Count

from main.models import *

register = template.Library()


@register.inclusion_tag('parts/sidebar.html', takes_context=True)
def sidebar_view(context):
    ctx = {
        # 'categories': NotesCategory.objects.annotate(total=Count('note')).filter(total__gt=0, note__user=context['user']),
        'categories': NotesCategory.objects.annotate(total=Count('note')).filter(user=context['user']),
    }

    if 'cat_selected' in context:
        ctx['cat_selected'] = context['cat_selected']
    else:
        ctx['cat_selected'] = ''
    return ctx