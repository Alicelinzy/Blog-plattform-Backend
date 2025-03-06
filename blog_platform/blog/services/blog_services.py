from django.db import transaction
from rest_framework import status
from blog.repositories.blog_repository import BlogRepository
from blog.repositories.category_repository import CategoryRepository
from accounts.repositories.author_repository import AuthorRepository


class APIResponse:
    def __init__(self, success: bool, data=None, message="", status=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.status = status

    def __str__(self):
        return f"APIResponse(success={self.success}, data={self.data}, message={self.message}, status={self.status})"


class BlogService:
    @staticmethod
    def create_blog(user, title: str, content: str, category_id: int = None):
        """Handles blog creation logic."""

        if not title or not content:
            return APIResponse(False, None, "Title and content are required.", status.HTTP_400_BAD_REQUEST)

        if not hasattr(user, "author"):
            return APIResponse(False, None, "Only authors can create blogs.", status.HTTP_403_FORBIDDEN)

        category = None
        if category_id:
            category_response = CategoryRepository.get_category_by_id(category_id)  #
            if not category_response.success:
                return APIResponse(False, None, "Category not found.", status.HTTP_404_NOT_FOUND)
            category = category_response.data

            response = BlogRepository.create_blog(user, title, content, category["id"] if category else None)
        
        if response:
            return APIResponse(
                response.success,
                response.data,
                response.message,
                status.HTTP_201_CREATED if response.success else status.HTTP_400_BAD_REQUEST
            )

        return APIResponse(False, None, "Something went wrong.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_blog_by_id(blog_id: int):
        """Retrieve a blog by its ID."""
        response = BlogRepository.get_blog_by_id(blog_id)
        return APIResponse(
            response.success,
            response.data,
            response.message,
            status.HTTP_200_OK if response.success else status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def get_all_blogs():
        """Retrieve all blogs."""
        response = BlogRepository.get_all_blogs()
        return APIResponse(
            response.success,
            response.data,
            response.message,
            status.HTTP_200_OK if response.success else status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def update_blog(blog_id: int, **kwargs):
        try:
            if not kwargs:
                return APIResponse(False, None, "No update data provided.", status.HTTP_400_BAD_REQUEST)

            if "title" in kwargs and not kwargs["title"]:
                return APIResponse(False, None, "Title cannot be empty.", status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                response = BlogRepository.update_blog(blog_id, **kwargs)
                return APIResponse(
                    response.success,
                    response.data,
                    response.message,
                    status.HTTP_200_OK if response.success else status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Error in update_blog: {e}")
            return APIResponse(False, None, "Failed to update blog.", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete_blog(blog_id: int):
        """Delete a blog."""
        try:
            with transaction.atomic():
                response = BlogRepository.delete_blog(blog_id)
                return APIResponse(
                    response.success,
                    None,
                    response.message,
                    status.HTTP_200_OK if response.success else status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Error in delete_blog: {e}")
            return APIResponse(False, None, "Failed to delete blog.", status.HTTP_500_INTERNAL_SERVER_ERROR)