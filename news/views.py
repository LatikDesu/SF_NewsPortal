from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news.models import Post, PostCategory, Comment
from accounts.models import Author


# Create your views here.
class PostView(ListView):
    model = Post
    title = 'DesuNews - blog'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostView, self).get_context_data()
        context['categories'] = PostCategory.objects.all()
        context['title'] = self.title
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['categories'] = PostCategory.objects.all()
        context['title'] = f'{self.object.title}'
        context['author'] = Author.objects.filter(pk=self.object.author_id).first()
        context['comments'] = Comment.objects.filter(post=self.object.id)
        return context
