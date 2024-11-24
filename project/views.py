from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django_htmx.http import HttpResponseClientRedirect
from django.shortcuts import render, get_object_or_404
from .models import Post


class HomeView(TemplateView):
    template_name = "home.html"


class LoginView(DjangoLoginView):
    template_name = "auth/login.html"

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseClientRedirect(self.get_success_url())


class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return HttpResponseClientRedirect(self.get_success_url())


def PostDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True).prefetch_related(
        'children__children', 'likes__author', 'children__likes__author'
    )

    # Pre-process comments and nested replies
    for comment in comments:
        process_comment_likes(comment)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


def process_comment_likes(comment):
    """Recursively process likes for a comment and its replies."""
    comment.like_count = comment.likes.filter(like_type='like').count()
    comment.heart_count = comment.likes.filter(like_type='heart').count()
    comment.laugh_count = comment.likes.filter(like_type='laugh').count()
    comment.like_users = comment.likes.filter(like_type='like').values_list('author__username', flat=True)
    comment.heart_users = comment.likes.filter(like_type='heart').values_list('author__username', flat=True)
    comment.laugh_users = comment.likes.filter(like_type='laugh').values_list('author__username', flat=True)

    # Process children recursively
    for reply in comment.children.all():
        process_comment_likes(reply)
