from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "home.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect("login")  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, "auth/register.html", {"form": form})