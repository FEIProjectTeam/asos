from django.test import TestCase
from django.contrib.auth import get_user_model
from project.models import Category, Post, Comment, Like, LikeType

User = get_user_model()


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(author=self.user, category=self.category, title='Test Post', description='Test Desc')
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='Test Comment')

    def test_str_methods(self):
        self.assertEqual(str(self.category), 'Test Category')
        self.assertEqual(str(self.post), 'Test Post')
        self.assertEqual(str(self.comment), 'Test Comment')

    def test_like_constraints(self):
        # Like on a post
        like = Like.objects.create(author=self.user, post=self.post, like_type=LikeType.LIKE)
        self.assertIsNotNone(like.id)

        # Attempt to create a second identical like on the same post by the same user
        with self.assertRaises(Exception):
            Like.objects.create(author=self.user, post=self.post, like_type=LikeType.LIKE)

    def test_comment_hierarchy(self):
        reply = Comment.objects.create(post=self.post, author=self.user, parent=self.comment, text='Reply Comment')
        self.assertEqual(reply.parent, self.comment)
