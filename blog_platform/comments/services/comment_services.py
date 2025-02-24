from comments.repositories.comment_repository import CommentRepository
from comments.serializers import CommentSerializer
from base.utils.responses import APIResponse
from rest_framework import status


class CommentService:
    @staticmethod
    def create_comment(data):
        if not all([data.get("blog_id"), data.get("user_type"), data.get("user_id"), data.get("content")]):
            return APIResponse(False, None, "Missing required fields.", status.HTTP_400_BAD_REQUEST)

        response = CommentRepository.create_comment(data)
        if response.success and response.data:
            serialized_data = CommentSerializer(response.data).data
            return APIResponse(True, serialized_data, response.message, status.HTTP_201_CREATED)
        return response

    @staticmethod
    def get_comment_by_id(comment_id):
        if not comment_id:
            return APIResponse(False, None, "Comment ID is required.", status.HTTP_400_BAD_REQUEST)

        response = CommentRepository.get_comment_by_id(comment_id)
        if response.success and response.data:
            serialized_data = CommentSerializer(response.data).data
            return APIResponse(True, serialized_data, response.message, status.HTTP_200_OK)
        return response

    @staticmethod
    def get_all_comments():
        response = CommentRepository.get_all_comments()
        if response.success and response.data:
            serialized_data = CommentSerializer(response.data, many=True).data
            return APIResponse(True, serialized_data, response.message, status.HTTP_200_OK)
        return response

    @staticmethod
    def get_comments_by_blog(blog_id):
        if not blog_id:
            return APIResponse(False, None, "Blog ID is required.", status.HTTP_400_BAD_REQUEST)

        response = CommentRepository.get_comments_by_blog(blog_id)
        if response.success and response.data:
            serialized_data = CommentSerializer(response.data, many=True).data
            return APIResponse(True, serialized_data, response.message, status.HTTP_200_OK)
        return response

    @staticmethod
    def get_replies(parent_comment_id):
        if not parent_comment_id:
            return APIResponse(False, None, "Parent comment ID is required.", status.HTTP_400_BAD_REQUEST)

        response = CommentRepository.get_replies(parent_comment_id)
        if response.success and response.data:
            serialized_data = CommentSerializer(response.data, many=True).data
            return APIResponse(True, serialized_data, response.message, status.HTTP_200_OK)
        return response

    @staticmethod
    def update_comment(comment_id, data):
        if not comment_id or not data:
            return APIResponse(False, None, "Comment ID and update data are required.", status.HTTP_400_BAD_REQUEST)

        response = CommentRepository.update_comment(comment_id, data)
        if response.success and response.data:
            serialized_data = CommentSerializer(response.data).data
            return APIResponse(True, serialized_data, response.message, status.HTTP_200_OK)
        return response

    @staticmethod
    def delete_comment(comment_id):
        if not comment_id:
            return APIResponse(False, None, "Comment ID is required.", status.HTTP_400_BAD_REQUEST)

        return CommentRepository.delete_comment(comment_id)
