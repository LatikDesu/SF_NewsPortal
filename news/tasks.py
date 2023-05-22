import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Category, Post


@shared_task
def send_email_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()

    link = f'{settings.DOMAIN_NAME}{post.get_absolute_url()}'
    subscribers_emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string(
        'mail/email_post_created.html',
        {
            'title': post.title,
            'description': post.description,
            'link': link
        }
    )

    msg = EmailMultiAlternatives(
        subject=f"DesuNews | Новые статьи в категории: {categories.first()}",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_notification():
    today = datetime.datetime.now(tz=timezone.utc)
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time__gte=last_week)
    categories = set(posts.values_list('postcategory', flat=True))
    subscribers = set(
        Category.objects.filter(postcategory__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'mail/email_weekly.html',
        {
            'title': 'DesuNews | Статьи за неделю',
            'link': settings.DOMAIN_NAME,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
