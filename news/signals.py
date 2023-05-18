from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from SF_NewsPortal import settings

from .models import PostCategory
from .tasks import send_email_post


@receiver(m2m_changed, sender=PostCategory)
def notify_category_subscribers(sender, instance, **kwargs):
    send_email_post.delay(instance.pk)

    # if kwargs['action'] == 'post_add':
    #     categories = instance.category.all()
    #     link = f'{settings.DOMAIN_NAME}{instance.get_absolute_url()}'
    #     subscribers_emails = []
    #
    #     for category in categories:
    #         subscribers = category.subscribers.all()
    #         subscribers_emails += [s.email for s in subscribers]
    #
    #     html_content = render_to_string(
    #         'mail/email_post_created.html',
    #         {
    #             'title': instance.title,
    #             'description': instance.description,
    #             'link': link
    #         }
    #     )
    #
    #     msg = EmailMultiAlternatives(
    #         subject=f"DesuNews | Новые статьи в категории: {categories.first()}",
    #         body='',
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         to=subscribers_emails,
    #     )
    #
    #     msg.attach_alternative(html_content, 'text/html')
    #     msg.send()
