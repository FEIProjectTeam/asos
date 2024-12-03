from collections import defaultdict
from typing import Any

from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Q, Value, Prefetch
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django_htmx.http import HttpResponseClientRedirect
from django.shortcuts import get_object_or_404

from .forms import CommentForm
from .models import Post, Comment, LikeType, Like


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


class PostDetailView(TemplateView):
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        post_id: int = kwargs["post_id"]
        likes_prefetch = Prefetch(
            "likes", queryset=Like.objects.all().select_related("author")
        )
        post = get_object_or_404(
            Post.objects.filter(id=post_id)
            .select_related("category")
            .prefetch_related("attachments", likes_prefetch)
            .annotate(
                like_count=Count(
                    "likes", filter=Q(likes__like_type=LikeType.LIKE), distinct=True
                ),
                heart_count=Count(
                    "likes", filter=Q(likes__like_type=LikeType.HEART), distinct=True
                ),
                laugh_count=Count(
                    "likes", filter=Q(likes__like_type=LikeType.LAUGH), distinct=True
                ),
                like_authors=ArrayAgg(
                    "likes__author__username",
                    filter=Q(likes__like_type=LikeType.LIKE),
                    default=Value([]),
                ),
                heart_authors=ArrayAgg(
                    "likes__author__username",
                    filter=Q(likes__like_type=LikeType.HEART),
                    default=Value([]),
                ),
                laugh_authors=ArrayAgg(
                    "likes__author__username",
                    filter=Q(likes__like_type=LikeType.LAUGH),
                    default=Value([]),
                ),
            )
        )
        comments = (
            Comment.objects.filter(post=post)
            .select_related("author")
            .prefetch_related("likes__author")
            .annotate(
                like_count=Count(
                    "likes", filter=Q(likes__like_type=LikeType.LIKE), distinct=True
                ),
                heart_count=Count(
                    "likes", filter=Q(likes__like_type=LikeType.HEART), distinct=True
                ),
                laugh_count=Count(
                    "likes", filter=Q(likes__like_type=LikeType.LAUGH), distinct=True
                ),
                like_authors=ArrayAgg(
                    "likes__author__username",
                    filter=Q(likes__like_type=LikeType.LIKE),
                    default=Value([]),
                ),
                heart_authors=ArrayAgg(
                    "likes__author__username",
                    filter=Q(likes__like_type=LikeType.HEART),
                    default=Value([]),
                ),
                laugh_authors=ArrayAgg(
                    "likes__author__username",
                    filter=Q(likes__like_type=LikeType.LAUGH),
                    default=Value([]),
                ),
            )
        )
        replies = defaultdict(list)
        top_lvl_comments = []
        comment_count = 0
        for comment in comments:
            comment_count += 1
            if comment.parent:
                replies[comment.parent.id].append(comment)
            else:
                top_lvl_comments.append(comment)
        kwargs["post"] = post
        kwargs["comment_count"] = comment_count
        kwargs["top_lvl_comments"] = top_lvl_comments
        kwargs["replies"] = replies
        return super().get_context_data(**kwargs)


class CommentFormView(FormView):
    template_name = "comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        post_id: int = self.kwargs["post_id"]
        parent_id: int | None = self.kwargs.get("parent_id")
        comment = Comment(
            post_id=post_id,
            author=self.request.user,
            parent_id=parent_id,
            **form.cleaned_data,
        )
        comment.save()
        return HttpResponseClientRedirect(
            reverse_lazy("post_detail", kwargs={"post_id": self.kwargs["post_id"]})
        )
