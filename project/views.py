from collections import defaultdict
from typing import Any

from django.contrib.auth import (
    get_user_model,
    login,
    authenticate,
    update_session_auth_hash,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Q, Value, Prefetch
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView, CreateView
from django_htmx.http import HttpResponseClientRedirect
from django_htmx.http import retarget

from .forms import ChangeProfileForm, ChangePasswordForm, UserCreationForm
from .forms import CommentForm, LikeForm
from .forms import PostForm, AttachmentForm
from .models import Comment, LikeType, Like, Attachment
from .models import Post


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"
    login_url = reverse_lazy("home")


class SettingsPass(LoginRequiredMixin, TemplateView):
    template_name = "settingsPass.html"
    login_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        changePasswordForm = ChangePasswordForm(user=request.user)
        return render(
            request,
            self.template_name,
            {
                "change_password_form": changePasswordForm,
            },
        )

    def post(self, request, *args, **kwargs):
        changePasswordForm = ChangePasswordForm(user=request.user, data=request.POST)
        if changePasswordForm.is_valid():
            changePasswordForm.save()
            update_session_auth_hash(
                request, request.user
            )  # Important to keep the user logged in
            return render(
                request,
                self.template_name,
                {
                    "change_password_form": ChangePasswordForm(user=request.user),
                    "success": "Password updated successfully!",
                },
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    "change_password_form": changePasswordForm,
                    "error": "Password not updated.",
                },
                status=400,
            )


class SettingsProfile(LoginRequiredMixin, TemplateView):
    template_name = "settingsProfile.html"
    login_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        changeProfileForm = ChangeProfileForm(instance=request.user)
        return render(
            request,
            self.template_name,
            {
                "change_profile_form": changeProfileForm,
            },
        )

    def post(self, request, *args, **kwargs):
        changeProfileForm = ChangeProfileForm(request.POST, instance=request.user)
        if changeProfileForm.is_valid():
            changeProfileForm.save()
            return render(
                request,
                self.template_name,
                {
                    "change_profile_form": changeProfileForm,
                    "success": "Profile updated successfully!",
                },
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    "change_profile_form": changeProfileForm,
                    "error": "Profile not updated.",
                },
                status=400,
            )


class HomeView(TemplateView):
    template_name = "home.html"


class LoginView(DjangoLoginView):
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return retarget(response, "#modal-placeholder")

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
    template_name = "post/post_detail.html"

    def _annotate_like_count(self, like_type: LikeType = LikeType.LIKE):
        return Count("likes", filter=Q(likes__like_type=like_type), distinct=True)

    def _annotate_like_authors(self, like_type: LikeType = LikeType.LIKE):
        return ArrayAgg(
            "likes__author__username",
            filter=Q(likes__like_type=like_type),
            default=Value([]),
        )

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
                like_count=self._annotate_like_count(),
                heart_count=self._annotate_like_count(LikeType.HEART),
                laugh_count=self._annotate_like_count(LikeType.LAUGH),
                like_authors=self._annotate_like_authors(),
                heart_authors=self._annotate_like_authors(LikeType.HEART),
                laugh_authors=self._annotate_like_authors(LikeType.LAUGH),
            )
        )
        comments = (
            Comment.objects.filter(post=post)
            .select_related("author")
            .prefetch_related("likes__author")
            .annotate(
                like_count=self._annotate_like_count(),
                heart_count=self._annotate_like_count(LikeType.HEART),
                laugh_count=self._annotate_like_count(LikeType.LAUGH),
                like_authors=self._annotate_like_authors(),
                heart_authors=self._annotate_like_authors(LikeType.HEART),
                laugh_authors=self._annotate_like_authors(LikeType.LAUGH),
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


class CommentFormView(LoginRequiredMixin, FormView):
    template_name = "comment.html"
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            reverse("post_detail", kwargs={"post_id": self.kwargs["post_id"]})
        )

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


class BaseLikeView(LoginRequiredMixin, View):
    form_class = LikeForm

    def get(self, request, post_id: int, *args, **kwargs):
        return HttpResponseRedirect(reverse("post_detail", kwargs={"post_id": post_id}))


class PostLikeView(BaseLikeView):
    def post(self, request, post_id: int, *args, **kwargs):
        form = self.form_class(request.POST)
        if not Post.objects.filter(id=post_id).exists():
            raise Http404

        if form.is_valid():
            like = Like.objects.filter(post_id=post_id, author=request.user).first()
            like_type = form.cleaned_data["like_type"]
            if like:
                if like.like_type == like_type:
                    like.delete()
                else:
                    like.like_type = like_type
                    like.save()
            else:
                Like(post_id=post_id, author=request.user, like_type=like_type).save()
        return HttpResponseClientRedirect(
            reverse("post_detail", kwargs={"post_id": post_id})
        )


class CommentLikeView(BaseLikeView):
    def post(self, request, post_id: int, comment_id: int, *args, **kwargs):
        form = self.form_class(request.POST)
        if (
            not Post.objects.filter(id=post_id).exists()
            or not Comment.objects.filter(post_id=post_id, id=comment_id).exists()
        ):
            raise Http404

        if form.is_valid():
            like = Like.objects.filter(
                comment_id=comment_id, author=request.user
            ).first()
            like_type = form.cleaned_data["like_type"]
            if like:
                if like.like_type == like_type:
                    like.delete()
                else:
                    like.like_type = like_type
                    like.save()
            else:
                Like(
                    comment_id=comment_id, author=request.user, like_type=like_type
                ).save()
        return HttpResponseClientRedirect(
            reverse("post_detail", kwargs={"post_id": post_id})
        )


class CreatePost(TemplateView):
    template_name = "post/createPost.html"

    def get(self, request, *args, **kwargs):
        post_form = PostForm()
        attachment_form = AttachmentForm()
        return render(
            request,
            self.template_name,
            {"post_form": post_form, "attachment_form": attachment_form},
        )

    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist("file")
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            for file in files:
                Attachment.objects.create(post=post, file=file)

            return JsonResponse(
                {
                    "message": "Post and attachment created successfully!",
                    "post_id": post.id,
                }
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    "post_form": post_form.errors,
                },
                status=400,
            )

class ImageView(View):
    def get(self, request):

        # loadni obrazky a jebni ich do images_to_show a cislo dalsej strany do next_page

        return render(
            request,
            "partials/images.html",
            {"images": images_to_show, "page": next_page},
        )
