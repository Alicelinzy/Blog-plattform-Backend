import re
from django.db import transaction
from rest_framework import status
from accounts.repositories.author_repository import AuthorRepository
from accounts.serializers import AuthorSerializer
from accounts.services.user_serivces import UserService
from django.contrib.auth.models import User
from accounts.repositories.author_repository import RepositoryResponse
from accounts.models import Author
 

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
                required_fields = ["username", "password", "email", "first_name", "last_name"]
                for field in required_fields:
                    if field not in data:
                        return APIResponse(False, None, f"{field} is required", status.HTTP_400_BAD_REQUEST)
                existing_user = User.objects.filter(email=data.get('email')).first()
                if existing_user:
                    return APIResponse(False, None, f"User with email {data.get('email')} already exists", status.HTTP_400_BAD_REQUEST)
                user_data = {
                    "username": data.get("username"),
                    "password": data.get("password"),
                    "email": data.get("email"),
                    "first_name": data.get("first_name"),
                    "last_name": data.get("last_name")
                }
                """"validates email"""""
                
                if not AuthorService.validate_email(user_data["email"]):
                    return APIResponse(False, None, "Invalid email format", status.HTTP_400_BAD_REQUEST)
                
                new_user = User.objects.create_user(**user_data)
                if not new_user:
                    return APIResponse(False, None, "Failed to create user", status.HTTP_400_BAD_REQUEST)

                author_data = {
                    "user": new_user,
                    "bio": data.get("bio", ""),
                    "profile_picture": data.get("profile_picture", "") 
                }

                """"Create author"""""
                author_response = AuthorRepository.create_author(new_user, author_data)
                if not author_response.success:
                    return APIResponse(False, None, author_response.message, status.HTTP_400_BAD_REQUEST)

                serialized_author = AuthorSerializer(author_response.data).data
                return APIResponse(True, serialized_author, "Author created successfully", status.HTTP_201_CREATED)

        except Exception as e:
            return APIResponse(False, None, f"Error creating author in service: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_author_by_id(author_id):
        try:
            author = Author.objects.filter(user__id=author_id).first()
            if author:
                serialized_author = AuthorSerializer(instance=author).data
                return RepositoryResponse(True, serialized_author, "Author found.")
            return RepositoryResponse(False, None, "Author not found.")
        except Exception as e:
            return RepositoryResponse(False, None, "Error retrieving author: " + str(e))

    @staticmethod
    def get_all_authors():
        try:
            authors = Author.objects.all()
            serialized_authors = AuthorSerializer(instance=authors, many=True).data
            return RepositoryResponse(True, serialized_authors, "Authors retrieved successfully.")
        except Exception as e:
            print(f"Error retrieving authors: {e}")
            return RepositoryResponse(False, None, "Error retrieving authors.")

    @staticmethod
    def update_author(author_id, data):
        try:
            with transaction.atomic():
                author = Author.objects.filter(user__id=author_id).first()
                if not author:
                    return RepositoryResponse(False, None, "Author not found.")

                if "email" in data:
                    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                    if not re.match(email_pattern, data["email"]):
                        return RepositoryResponse(False, None, "Invalid email format.")

                    if Author.objects.exclude(user__id=author_id).filter(user__email=data["email"]).exists():
                        return RepositoryResponse(False, None, "Email already exists.")

                if "username" in data and Author.objects.exclude(user__id=author_id).filter(user__username=data["username"]).exists():
                    return RepositoryResponse(False, None, "Username already exists.")

                for key, value in data.items():
                    if hasattr(author.user, key):
                        setattr(author.user, key, value)
                    else:
                        setattr(author, key, value)

                author.user.save()
                author.save()

                serialized_author = AuthorSerializer(instance=author).data
                return RepositoryResponse(True, serialized_author, "Author updated successfully.")

        except Exception as e:
            return RepositoryResponse(False, None, "Error updating author: " + str(e))

    

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
