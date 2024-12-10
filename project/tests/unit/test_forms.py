from django.test import TestCase
from django.contrib.auth.models import User
from project.forms import CommentForm, PostForm, ChangePasswordForm
from project.models import Category


class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')

    def test_comment_form_valid(self):
        form = CommentForm(data={'text': 'A comment'})
        self.assertTrue(form.is_valid())

    def test_post_form_valid(self):
        form = PostForm(data={'title': 'Post Title', 'description': 'Post Desc', 'category': self.category.id})
        self.assertTrue(form.is_valid(), form.errors)

    def test_change_password_form(self):
        form = ChangePasswordForm(user=self.user, data={
            'old_password': 'testpass',
            'new_password': 'NewPass123!',
            'confirm_password': 'NewPass123!'
        })
        self.assertTrue(form.is_valid(), form.errors)
