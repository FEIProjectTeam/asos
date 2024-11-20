from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm


class HomeView(TemplateView):
    template_name = "home.html"


class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("home")
