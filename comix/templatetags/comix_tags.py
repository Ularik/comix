from django import template
from comix.models import Comments
from comix.models import Posters

register = template.Library()


@register.simple_tag()
def get_posters():
    return Posters.objects.all()


@register.inclusion_tag('comix/detail_comments_tag.html', takes_context=True)
def show_comments(context):
    comix = context['comix']
    comments = Comments.objects.filter(comix__pk=comix.id)
    return {'comments': comments}
