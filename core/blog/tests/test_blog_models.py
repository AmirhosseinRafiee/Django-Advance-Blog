from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from accounts.models import Profile
from ..models import Post

class TestPostModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email = "test@test.com", password = "a/@12345")
        self.profile = Profile.objects.get(user=self.user)
        self.post = Post.objects.create(
            author = self.profile,
            title = "this is title",
            content = "this is content",
            status = True,
            # category = None,
            published_date = datetime.now()
        )

    def test_create_post_with_valid_data(self):
        post = Post.objects.create(
            author = self.profile,
            title = "this is title",
            content = "this is content",
            status = True,
            # category = None,
            published_date = datetime.now()
        )
        self.assertTrue(Post.objects.get(pk=post.id))
        self.assertEqual(post.title, "this is title")

