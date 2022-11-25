from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from ...models import Post

"""
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def post_detail(request, id):
    post = get_object_or_404(Post, pk=id, status=True)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail": "item removed successfully"}, status=status.HTTP_204_NO_CONTENT)

"""

class PostListView(APIView):
    """ get a list of posts and create new post """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    """ return a list of posts """
    def get(self, request):
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    """ create a post with provided data """
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




class PostDetailView(APIView):
    """ get detail of the post and edit plus remove it """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, id):
        """ return the post data """
        post = get_object_or_404(Post, pk=id, status=True)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, id):
        """ edit the post data """
        post = get_object_or_404(Post, pk=id, status=True)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        """ delete the post object """
        post = get_object_or_404(Post, pk=id, status=True)
        post.delete()
        return Response({"detail": "item removed successfully"}, status=status.HTTP_204_NO_CONTENT)

