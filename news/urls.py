from django.urls import path

from .views import (AddComment, ArticleCreateView, ArticleDeleteView,
                    ArticleUpdateView, PostCreateView, PostDeleteView,
                    PostDetailView, PostUpdateView, PostView)

app_name = 'news'

urlpatterns = [
    path('', PostView.as_view(), name='news_list'),
    path("<int:pk>/", PostDetailView.as_view(), name="news_detail"),
    path('page/<int:page>', PostView.as_view(), name='paginator'),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),

    path('news/create/', PostCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),

    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
