from django.contrib import admin
from unicodedata import category

from .models import Post, Category, Comment, PostCategory


# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly = True


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'time', 'rating')
    inlines = [CategoryInline, CommentInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
