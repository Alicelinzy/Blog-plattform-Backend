import re
from django.db import transaction
from rest_framework import status
from accounts.repositories.author_repository import AuthorRepository
from accounts.serializers import AuthorSerializer
from accounts.services.user_serivces import UserService 
 

class APIResponse:
    def __init__(self, success: bool, data=None, message="", status=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.status = status

    def __str__(self):
        return f"APIResponse(success={self.success}, data={self.data}, message={self.message}, status={self.status})"


class AuthorService:
    @staticmethod
    def validate_email(email: str) -> bool:
        """ Validate email format """
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_pattern, email) is not None

    @staticmethod
    def create_author(data):
        try:
            with transaction.atomic():
                user_fields = ["username", "password", "email", "first_name", "last_name"]
                user_data = {field: data.get(field, "").strip() for field in user_fields}

                author_fields = ["bio", "profile_picture"]
                author_data = {
                    "bio": data.get("bio", "").strip(),
                    "profile_picture": data.get("profile_picture", None) 
                }

                """"validates email"""""
                
                if not AuthorService.validate_email(user_data["email"]):
                    return APIResponse(False, None, "Invalid email format", status.HTTP_400_BAD_REQUEST)

                """"Create our user first"""""
                user_response = UserService.create_user(user_data)
                if not user_response.success:
                    return APIResponse(False, None, user_response.message, user_response.status)

                user = user_response.data 

                """"Create author"""""
                author_response = AuthorRepository.create_author(user, author_data)
                if not author_response.success:
                    return APIResponse(False, None, author_response.message, status.HTTP_400_BAD_REQUEST)

                serialized_author = AuthorSerializer(author_response.data).data
                return APIResponse(True, serialized_author, "Author created successfully", status.HTTP_201_CREATED)

        except Exception as e:
            return APIResponse(False, None, f"Error creating author: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_author_by_id(author_id: int):
        response = AuthorRepository.get_author_by_id(author_id)
        if response.success:
            return APIResponse(True, response.data, response.message, status.HTTP_200_OK)
        return APIResponse(False, None, response.message, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_all_authors():
        response = AuthorRepository.get_all_authors()
        if response.success:
            return APIResponse(True, response.data, response.message, status.HTTP_200_OK)
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
            return APIResponse(True, response.data, response.message, status.HTTP_200_OK)

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
