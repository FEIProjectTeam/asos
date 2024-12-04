from django import forms
from django.forms import Form

from project.models import LikeType


class CommentForm(Form):
    text = forms.CharField()


class LikeForm(Form):
    like_type = forms.ChoiceField(choices=LikeType.choices)
