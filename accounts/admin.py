from django.contrib import admin

from accounts.models import Author

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'rating',)
