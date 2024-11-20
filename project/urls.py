from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import RegisterView
from django.contrib.auth.views import LogoutView
from project.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
