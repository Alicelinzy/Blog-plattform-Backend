from comments.models import Comment
from accounts.models import Author, Reader
from blog.models import Blog
from django.db import IntegrityError
from base.utils.responses import APIResponse
from rest_framework import status


class CommentRepository:
    @staticmethod
    def create_comment(data):
        try:
            blog = Blog.objects.filter(id=data.get("blog_id")).first()
            parent = Comment.objects.filter(id=data.get("parent_id")).first() if data.get("parent_id") else None
            
            author = Author.objects.filter(id=data.get("author_id")).first() if data.get("author_id") else None
            reader = Reader.objects.filter(id=data.get("reader_id")).first() if data.get("reader_id") else None

            if not blog or not data.get("content") or (not author and not reader):
                return APIResponse(False, None, "Invalid input data.", status.HTTP_400_BAD_REQUEST)

            
            comment = Comment.objects.create(
                blog=blog, 
                author=author, 
                reader=reader, 
                parent=parent, 
                content=data["content"]
            )
            return APIResponse(True, comment, "Comment created successfully.", status.HTTP_201_CREATED)
        
        except IntegrityError as e:
            return APIResponse(False, None, f"Database error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return APIResponse(False, None, f"Error creating comment: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_comment_by_id(comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            return APIResponse(False, None, "Comment not found.", status.HTTP_404_NOT_FOUND)
        return APIResponse(True, comment, "Comment found.", status.HTTP_200_OK)

    @staticmethod
    def get_all_comments():
        comments = Comment.objects.all()
        if not comments.exists():
            return APIResponse(False, None, "No comments found.", status.HTTP_404_NOT_FOUND)
        return APIResponse(True, comments, "Comments retrieved successfully.", status.HTTP_200_OK)

    @staticmethod
    def get_comments_by_blog(blog_id):
        blog = Blog.objects.filter(id=blog_id).first()
        if not blog:
            return APIResponse(False, None, "Blog not found.", status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(blog=blog)
        if not comments.exists():
            return APIResponse(False, None, "No comments found.", status.HTTP_404_NOT_FOUND)
        return APIResponse(True, comments, "Comments retrieved successfully.", status.HTTP_200_OK)

    @staticmethod
    def get_replies(parent_comment_id):
        parent = Comment.objects.filter(id=parent_comment_id).first()
        if not parent:
            return APIResponse(False, None, "Parent comment not found.", status.HTTP_404_NOT_FOUND)
        replies = Comment.objects.filter(parent=parent)
        if not replies.exists():
            return APIResponse(False, None, "No replies found.", status.HTTP_404_NOT_FOUND)
        return APIResponse(True, replies, "Replies retrieved successfully.", status.HTTP_200_OK)

    @staticmethod
    def update_comment(comment_id, data):
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            return APIResponse(False, None, "Comment not found.", status.HTTP_404_NOT_FOUND)

        updated_fields = {k: v for k, v in data.items() if k in ["content", "is_approved"]}
        if not updated_fields:
            return APIResponse(False, None, "No valid fields to update.", status.HTTP_400_BAD_REQUEST)

        for key, value in updated_fields.items():
            setattr(comment, key, value)

        comment.save()
        return APIResponse(True, comment, "Comment updated successfully.", status.HTTP_200_OK)

    @staticmethod
    def delete_comment(comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            return APIResponse(False, None, "Comment not found.", status.HTTP_404_NOT_FOUND)
        comment.delete()
        return APIResponse(True, None, "Comment deleted successfully.", status.HTTP_204_NO_CONTENT)
