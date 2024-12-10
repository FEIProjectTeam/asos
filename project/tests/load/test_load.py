import time
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from project.models import Post, Category

class TestLoad(TestCase):
    """
    A very basic "load test" using Django's own TestCase.
    This won't fully simulate real-world load testing but can show performance under simple loops.
    For real load tests, consider using external tools like Locust or JMeter.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='loaduser', password='testpass')
        self.category = Category.objects.create(name='Load Test Category')
        for i in range(50): # Create multiple posts
            Post.objects.create(author=self.user, category=self.category, title=f'Post {i}', description='Load test desc')
        self.url = reverse('post_list')

    def test_post_list_load(self):
        start_time = time.time()
        for _ in range(100):  # Simulate multiple requests
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Completed 100 requests in {duration:.2f} seconds")
