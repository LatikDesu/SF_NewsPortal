from django.contrib.auth.models import AbstractUser, Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now

from SF_NewsPortal import settings


class Author(AbstractUser):
    rating = models.FloatField(default=0)
    image = models.ImageField(upload_to='users_images', null=True, blank=True,
                              default='users_images/default_avatar.jpg')
    is_verified_email = models.BooleanField(default=False)
    about = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)

    # def update_rating(self):
    #     self.rating = 0
    #     for post in Post.objects.filter(author_id=self.id):
    #         self.rating += post.rating * 3
    #         for comment in Comment.objects.filter(post_id=post.id):
    #             self.rating += comment.rating
    #     for comment in Comment.objects.filter(user_id=self.id):
    #         self.rating += comment.rating
    #     self.save()

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

        app_label = 'accounts'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подверждение учетной записи для {self.user.username}'
        message = 'Для подверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )

        html_content = render_to_string(
            'mail/email_verification.html',
            {
                'username': self.user.username,
                'verification_link': verification_link,
            }
        )

        # send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[self.user.email],
        #     fail_silently=False,
        # )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.user.email],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    def is_expired(self):
        return True if now() >= self.expiration else False
