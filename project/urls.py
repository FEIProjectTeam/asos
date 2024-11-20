from django.contrib import admin
from django.urls import path
from project.views import HomeView

urlpatterns = [
    # path('', views.home, name='home'),  # Maps the root URL to the home view
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
]
