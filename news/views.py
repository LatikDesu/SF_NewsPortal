from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from news.forms import CommentForm
from news.models import Post
from accounts.models import Author
from .filters import PostFilter


# Create your views here.
class PostView(ListView):
    model = Post
    title = 'DesuNews - blog'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostView, self).get_context_data()
        context['title'] = self.title
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['title'] = f'{self.object.title}'
        context['author'] = Author.objects.filter(pk=self.object.author_id).first()
        return context


class AddComment(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        author = Author.objects.get(id=request.user.id)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.post = post
            form.user = author
            form.save()
        return redirect(reverse('news:news_detail', kwargs={'pk': pk}))
