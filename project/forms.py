from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm as DjUserCreationForm,
    UsernameField,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form

from project.models import LikeType
from .models import Post, Attachment


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Old Password",
                "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
            }
        ),
        validators=[password_validation.validate_password],
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        new_password = self.cleaned_data["new_password"]
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if not self.user.check_password(old_password):
            self.add_error("old_password", "Old password is incorrect!")

        if new_password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "User Name",
                    "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
                }
            ),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "category",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter title",
                    "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write your post...",
                    "class": "max-h-24 min-h-24 form-control rounded-2xl border-[2.5px] border-neutral-300 p-4",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control rounded-2xl border-[2.5px] border-neutral-300 p-4"
                }
            ),
        }


class CommentForm(Form):
    text = forms.CharField()


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]
        labels = {"file": ""}
        widgets = {
            "file": forms.FileInput(
                attrs={
                    "class": "file-input form-control w-48 h-48 mt-7 rounded-2xl border-[2.5px] border-neutral-300 p-4",
                    "id": "id_file",
                    "onchange": "previewImage(event)",
                },
            ),
        }


class LikeForm(Form):
    like_type = forms.ChoiceField(choices=LikeType.choices)


class UserCreationForm(DjUserCreationForm):
    field_order = ["username", "email", "password1", "password2"]
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and self._meta.model.objects.filter(email__iexact=email).exists():
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email
