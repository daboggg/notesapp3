from django import template
from main.models import *

register = template.Library()

@register.simple_tag()
def get_note_categories():
    return NotesCategory.objects.all()