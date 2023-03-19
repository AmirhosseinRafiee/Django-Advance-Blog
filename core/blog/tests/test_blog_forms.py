from django.test import TestCase
from datetime import datetime
from ..forms import PostFrom
from ..models import Category

class TestPostForm(TestCase):

    def test_post_form_with_valid_data(self):
        category_obj = Category.objects.create(name="test")
        form = PostFrom(data={
            "title": "this is title",
            "content": "this is content",
            "status": True,
            "category": category_obj,
            "published_date": datetime.now()
        })
        self.assertTrue(form.is_valid())

    def test_post_form_with_no_data(self):
        form = PostFrom(data={})
        self.assertFalse(form.is_valid())
