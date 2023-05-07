from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from accounts.models import Author
from news.forms import CommentForm, PostForm
from news.models import Post, Category
from SF_NewsPortal import settings

from .filters import PostFilter


class AddComment(LoginRequiredMixin, View):

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
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostView, self).get_context_data()
        context['title'] = self.title
        context['filterset'] = self.filterset
        context['categoryName'] = Category.objects.filter(id=self.kwargs.get('category_id')).first()
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
class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)

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
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)

    form_class = PostForm
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != request.user:
            return HttpResponseForbidden("You don't have permission to edit this post.")

        return super().get(request, *args, **kwargs)


# Post delete
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)

    model = Post
    success_url = reverse_lazy('news:news_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            return HttpResponseForbidden("You don't have permission to delete this post.")
        return self.post(request, *args, **kwargs)


# Article create
class ArticleCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)

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
class ArticleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)

    form_class = PostForm
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != request.user:
            return HttpResponseForbidden("You don't have permission to edit this post.")

        return super().get(request, *args, **kwargs)


# Post delete
class ArticleDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)

    model = Post
    success_url = reverse_lazy('news:news_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            return HttpResponseForbidden("You don't have permission to delete this post.")
        return self.post(request, *args, **kwargs)


@login_required
def subscribe_category(request, category_id):
    user = Author.objects.get(username=request.user)
    category = Category.objects.get(id=category_id)
    if not category.subscribers.filter(username=user):
        category.subscribers.add(user)
    else:
        category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))
