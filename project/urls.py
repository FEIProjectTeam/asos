from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register
from django.contrib.auth.views import LogoutView
from project.views import HomeView

urlpatterns = [
    # path('', views.home, name='home'),  # Maps the root URL to the home view
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirects to the home page after logout
]
