from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from project.views import (
    HomeView,
    LoginView,
    RegisterView,
    PostDetailView,
    CommentFormView,
    PostLikeView,
    CommentLikeView,
    PostCreateView,
    SettingsView,
    SettingsProfile,
    SettingsPass,
    PostListView,
)

urlpatterns = [
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/profile/", SettingsProfile.as_view(), name="settingsProfile"),
    path("settings/password/", SettingsPass.as_view(), name="settingsPass"),
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:post_id>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:post_id>/like/", PostLikeView.as_view(), name="post_like"),
    path(
        "post/<int:post_id>/comment/create/",
        CommentFormView.as_view(),
        name="add_comment",
    ),
    path(
        "post/<int:post_id>/comment/<int:parent_id>/create/",
        CommentFormView.as_view(),
        name="add_reply",
    ),
    path(
        "post/<int:post_id>/comment/<int:comment_id>/like/",
        CommentLikeView.as_view(),
        name="comment_like",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
