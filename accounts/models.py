from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from SF_NewsPortal.settings import MEDIA_URL


# from news.models import Post, Comment


# Create your models here.
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
