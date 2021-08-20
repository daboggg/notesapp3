from django import template

register = template.Library()


@register.inclusion_tag('parts/pagination.html', takes_context=True)
def pagination_view(context):
    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj'],
    }