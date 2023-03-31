from django.db import models
from django.contrib.auth.models import User
from .resources import *


# Create your models here.

class Author(models.Model):
    rating = models.FloatField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = 0
        for post in Post.objects.filter(author_id=self.id):
            self.rating += post.rating * 3
            for comment in Comment.objects.filter(post_id=post.id):
                self.rating += comment.rating
        for comment in Comment.objects.filter(user_id=self.user):
            self.rating += comment.rating
        self.save()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    type = models.CharField(max_length=2, choices=TYPE, default=news)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.description[:124:1] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title} ({self.type}): {self.time.strftime("%d.%m.%Y")}: {self.description[:20]}'

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

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
