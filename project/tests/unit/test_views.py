from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from project.models import Post, Category

User = get_user_model()

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(author=self.user, category=self.category, title='Test Post', description='Test Desc')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/post_detail.html')

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/post_list.html')
        self.assertIn(self.post, response.context['object_list'])
