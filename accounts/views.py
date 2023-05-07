from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from accounts.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from accounts.models import Author, EmailVerification
from news.models import Post


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = Author
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:login')
    success_message = 'Вы успешно зарегистрированы!'


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['posts'] = Post.objects.filter(author=self.request.user).order_by('-time')
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class EmailVerificationView(LoginRequiredMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'accounts/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = Author.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
