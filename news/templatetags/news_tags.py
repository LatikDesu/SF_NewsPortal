from django import template

from news.models import Category, Post

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.inclusion_tag('news/tags/last_news.html')
def get_last_posts(count=3):
    posts = Post.objects.order_by("-id")[:count]
    return {"last_posts": posts}
