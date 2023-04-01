from django.urls import path

from .views import PostView, PostDetailView, AddComment

app_name = 'news'

urlpatterns = [
    path('', PostView.as_view(), name='news_list'),
    path("<int:pk>/", PostDetailView.as_view(), name="news_detail"),
    path('page/<int:page>/', PostView.as_view(), name='paginator'),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
]
