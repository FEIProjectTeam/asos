from django import forms
from django.forms import Form

from project.models import LikeType
from .models import Post, Attachment


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
        labels = {
            "file": ""
        }
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
