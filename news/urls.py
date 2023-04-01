from django.urls import path

from .views import PostView, PostDetailView

app_name = 'news'

urlpatterns = [
    path('', PostView.as_view(), name='news_list'),
    path("<int:pk>/", PostDetailView.as_view(), name="news_detail"),

]
