from rest_framework import serializers
from comments.models import Comment
from accounts.models import Author, Reader
from blog.models import Blog

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.name if hasattr(obj, "name") else str(obj)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  
    blog_title = serializers.CharField(source="blog.title", read_only=True)  
    replies = serializers.SerializerMethodField()  

    class Meta:
        model = Comment
        fields = ["id", "blog", "blog_title", "user", "parent", "content", "is_approved", "created_at", "updated_at", "replies"]

    def get_replies(self, obj):
        """Retrieve nested replies"""
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data if replies.exists() else []
