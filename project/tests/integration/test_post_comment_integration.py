from django.test import TestCase
from django.urls import reverse
from project.models import Post, User, Comment, Category

class TestPostCommentIntegration(TestCase):
    def setUp(self):
        # Create necessary objects
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Test Category")
        self.client.login(username="testuser", password="password123")
        
        # Create a post with the required category
        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Test Post",
            description="Test description"
        )
        self.comment_url = reverse('add_comment', kwargs={'post_id': self.post.id})

    def test_create_comment(self):
        response = self.client.post(
            self.comment_url,
            {'text': 'Integration Comment'},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('HX-Redirect', response.headers)
        self.assertTrue(Comment.objects.filter(post=self.post, text='Integration Comment').exists())
