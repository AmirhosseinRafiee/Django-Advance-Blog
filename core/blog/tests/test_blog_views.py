from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime
from accounts.models import Profile
from ..models import Post

class TestBlogView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(email="test@test.com", password="a/@12345")
        self.profile = Profile.objects.get(user=self.user)
        self.post = Post.objects.create(
            author = self.profile,
            title = "this is title",
            content = "this is content",
            status = True,
            # category = None,
            published_date = datetime.now()
        )
    
    def test_blog_index_url_successful_response(self):
        url = reverse("blog:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, template_name="index.html")
        self.assertTrue(str(response.content).find('index'))

    def test_blog_detail_url_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse("blog:post-detail", kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_url_anonymouse_response(self):
        url = reverse("blog:post-detail", kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    




