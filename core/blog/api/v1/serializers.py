from rest_framework import serializers
from ...models import Post, Category

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id','author','title','content','snippet','category','status','relative_url','absolute_url','created_date','published_date')
        # read_only_fields = ('content',)

    def get_absolute_url(self, post):
        request = self.context.get('request')
        return request.build_absolute_uri(post.pk)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category 
        fields = ('id', 'name')