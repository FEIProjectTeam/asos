from django import forms
from django.forms import Form


class CommentForm(Form):
    text = forms.CharField()
