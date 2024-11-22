from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from project.views import HomeView, LoginView, RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
