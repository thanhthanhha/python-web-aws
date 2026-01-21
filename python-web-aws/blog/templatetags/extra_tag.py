from django import template
from blog.models import Comment

register = template.Library()

@register.filter
def dictitem(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_value_in_qs(queryset):
    replies = Comment.objects.filter(reply=queryset)
    return replies