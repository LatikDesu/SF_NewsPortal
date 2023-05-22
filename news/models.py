from django.core.cache import cache
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

import accounts.models

from .resources import *


class Category(models.Model):
    name = models.CharField("Категория", max_length=255, unique=True)
    description = models.TextField("Описание")
    subscribers = models.ManyToManyField(accounts.models.Author, blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    type = models.CharField(max_length=2, choices=TYPE, default=news)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = HTMLField()
    rating = models.FloatField(default=0)
    draft = models.BooleanField("Черновик", default=False)
    poster = models.ImageField("Постер", upload_to="news", null=True, blank=True)

    author = models.ForeignKey(accounts.models.Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def get_comments(self):
        return self.comment_set.filter(parent__isnull=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title} ({self.type}): {self.time.strftime("%d.%m.%Y")}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title}: {self.category.name}'


class Comment(models.Model):
    text = models.TextField()
    rating = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )

    post = models.ForeignKey(Post, verbose_name="Статья", on_delete=models.CASCADE)
    user = models.ForeignKey(accounts.models.Author, verbose_name="Пользователь", on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.post.title} - {self.user}'
