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
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("post/<int:post_id>/", PostDetailView.as_view(), name="post_detail"),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
