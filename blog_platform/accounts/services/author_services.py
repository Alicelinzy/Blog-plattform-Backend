import re
from django.db import transaction
from rest_framework import status
from accounts.repositories.author_repository import AuthorRepository
from accounts.serializers import AuthorSerializer  


class APIResponse:
    def __init__(self, success: bool, data=None, message="", status=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.status = status
       


class AuthorService:
    @staticmethod
    def validate_email(email):
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    @staticmethod
    def create_author(username: str, password: str, email: str):
        if not all([username, password, email]):
            return APIResponse(False, None, "All fields are required", status.HTTP_400_BAD_REQUEST)

        if not AuthorService.validate_email(email):
            return APIResponse(False, None, "Invalid email format", status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return APIResponse(False, None, "Password must be at least 8 characters", status.HTTP_400_BAD_REQUEST)

        response = AuthorRepository.create_author({"username": username, "password": password, "email": email})

        if response.success:
            serialized_author = AuthorSerializer(response.data).data 
        else:
            serialized_author = None

        return APIResponse(response.success, serialized_author, response.message, status.HTTP_201_CREATED if response.success else status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_author_by_id(author_id: int):
        response = AuthorRepository.get_author_by_id(author_id)
        if response.success:
            serialized_author = AuthorSerializer(response.data).data 
            return APIResponse(True, serialized_author, response.message, status.HTTP_200_OK)
        return APIResponse(False, None, response.message, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_all_authors():
        response = AuthorRepository.get_all_authors()
        if response.success:
            serialized_authors = AuthorSerializer(response.data, many=True).data  # Serialize the queryset
            return APIResponse(True, serialized_authors, response.message, status.HTTP_200_OK)
        return APIResponse(False, None, response.message, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_author(author_id: int, **kwargs):
        if not kwargs:
            return APIResponse(False, None, "No fields provided to update", status.HTTP_400_BAD_REQUEST)

        response = AuthorRepository.get_author_by_id(author_id)
        if not response.success:
            return APIResponse(False, None, "Author not found", status.HTTP_404_NOT_FOUND)

        if "email" in kwargs:
            if not AuthorService.validate_email(kwargs["email"]):
                return APIResponse(False, None, "Invalid email format", status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            response = AuthorRepository.update_author(author_id, kwargs)

        if response.success:
            serialized_author = AuthorSerializer(response.data).data  # Serialize updated author
            return APIResponse(True, serialized_author, response.message, status.HTTP_200_OK)

        return APIResponse(False, None, response.message, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_author(author_id: int):
        response = AuthorRepository.get_author_by_id(author_id)
        if not response.success:
            return APIResponse(False, None, "Author not found", status.HTTP_404_NOT_FOUND)

        if hasattr(response.data, "blog_set") and response.data.blog_set.exists():
            return APIResponse(False, None, "Cannot delete author with existing blogs", status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            response = AuthorRepository.delete_author(author_id)

        return APIResponse(response.success, None, response.message, status.HTTP_200_OK if response.success else status.HTTP_400_BAD_REQUEST)
