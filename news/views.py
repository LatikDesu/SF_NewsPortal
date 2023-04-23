from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from accounts.models import Author
from news.forms import CommentForm, PostForm
from news.models import Post
from SF_NewsPortal import settings

from .filters import PostFilter


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


# Posts list
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


# Posts details
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['title'] = f'{self.object.title}'
        context['author'] = Author.objects.filter(pk=self.object.author_id).first()
        return context


# Posts create
class PostCreateView(CreateView):
    form_class = PostForm
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['TINYMCE_JS_URL'] = settings.TINYMCE_JS_URL
        return context

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'news'
        news.author = Author.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        invalid_fields = list(form.errors.keys())
        errors = form.errors.as_data()
        print(errors)
        print(f"Некоторые поля формы не прошли валидацию: {invalid_fields}")
        return super().form_invalid(form)


# Post update
class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post


# Post delete
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('news:news_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Article create
class ArticleCreateView(CreateView):
    form_class = PostForm
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['TINYMCE_JS_URL'] = settings.TINYMCE_JS_URL
        return context

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'article'
        news.author = Author.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        invalid_fields = list(form.errors.keys())
        errors = form.errors.as_data()
        print(errors)
        print(f"Некоторые поля формы не прошли валидацию: {invalid_fields}")
        return super().form_invalid(form)


# Article update
class ArticleUpdateView(UpdateView):
    form_class = PostForm
    model = Post


# Post delete
class ArticleDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('news:news_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
