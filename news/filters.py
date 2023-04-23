from django import forms
from django_filters import (CharFilter, DateTimeFilter, FilterSet,
                            ModelChoiceFilter)

from .models import Category, Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = ('title', 'author',)

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                      "max_length": "50",
                                      "type": "text",
                                      "placeholder": "Поиск по названию",
                                      })
    )

    author = CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                      "max_length": "50",
                                      "type": "text",
                                      "placeholder": "Поиск по автору",
                                      }),

    )

    time = DateTimeFilter(
        field_name='time',
        lookup_expr='gt',
        label='Начиная с указанной даты',
        widget=forms.TextInput(attrs={"class": " form-control form-control-lg",
                                      "type": "date",
                                      }),
    )
    # category = ModelChoiceFilter(
    #     field_name='category',
    #     queryset=Category.objects.all(),
    #     label='',
    #     empty_label='Выбрать категорию',
    #     widget=forms.Select(attrs={"class": "form-control form-control-lg",
    #                                "style": "background: #222222; "})
    # )
