from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    blog_title = serializers.CharField(source="blog.title", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "blog", "blog_title", "user", "parent", "content", "is_approved", "created_at", "updated_at", "replies"]

    def get_user(self, obj):
        if obj.user_role == "author":
            return {"id": obj.user.id, "username": obj.user.user.username, "role": "author"}
        elif obj.user_role == "reader":
            return {"id": obj.user.id, "username": obj.user.user.username, "role": "reader"}
        return None

    def get_replies(self, obj):
        """Retrieve nested replies"""
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data if replies.exists() else []
