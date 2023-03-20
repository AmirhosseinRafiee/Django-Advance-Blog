from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from datetime import datetime
import pytest
from accounts.models import Profile
from ..models import Post

# @pytest.fixture
# def client():
#     client = APIClient()
#     return client

@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(email="test@test.com", password="a/@12345", is_verified=True)
    return user

@pytest.fixture
def post_object(common_user):
    profile = Profile.objects.get(user=common_user)
    post = Post.objects.create(author=profile, title="test title", content="test content", status=True, published_date=datetime.now())
    return post

@pytest.mark.django_db
class TestPostApi:
    client = APIClient()

    def test_get_post_list_response_200_status(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_post_detail_response_200_status(self, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={'pk': post.id})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "status": True,
            "published_date": datetime.now()
        }
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_delete_post_response_401_status(self, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        
        response = self.client.delete(url)        
        assert response.status_code == 401
        # assert Post.objects.filter(id=post.id).exists()

    def test_edit_post_response_401_status(self, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        data = {
            "title": "new test title",
            "content": "new test content",
            "status": True,
            "published_date": datetime.now()
        }
        response = self.client.put(url, data=data)
        assert response.status_code == 401
        data2 ={
            "title": "edited title"
        }
        response = self.client.patch(url, data=data2)
        assert response.status_code == 401

    # user is authenticated from force_authenticate called
    def test_create_post_response_201_status(self, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "status": True,
            "published_date": datetime.now()
        }
        self.client.force_authenticate(user=common_user)
        response = self.client.post(url, data)
        assert response.status_code == 201
        assert Post.objects.get(title="test title")
    
    def test_create_post_invalid_data_response_400_status(self, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
        }
        response = self.client.post(url, data)
        assert response.status_code == 400 

    def test_delete_post_response_200_status(self, post_object, common_user):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        response = self.client.delete(url)     
        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()

    def test_edit_post_response_200_status(self, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        data = {
            "title": "new test title",
            "content": "new test content",
            "status": True,
            "published_date": datetime.now()
        }
        response = self.client.put(url, data=data)
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "new test title"
        data2 ={
            "title": "edited title"
        }
        response = self.client.patch(url, data=data2)
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "edited title"