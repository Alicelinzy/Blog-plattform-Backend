from accounts.models import Author
from accounts.serializers import AuthorSerializer
from django.db import IntegrityError, transaction
import re
from django.contrib.auth import get_user_model
User = get_user_model() 


class RepositoryResponse:
    def __init__(self, success: bool, data=None, message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return f"(success={self.success}, data={self.data}, message={self.message})"


class AuthorRepository:
    @staticmethod
    def create_author(user, author_data):
        try:
            with transaction.atomic():
                if isinstance(user, int):
                 user = User.objects.filter(id=user).first()
                if not user:
                    return RepositoryResponse(False, None, "User not found.")
                if Author.objects.filter(user=user).exists():
                    return RepositoryResponse(False, None, "Author already exists for this user.")
                
                author = Author.objects.create(
                    user=user,
                    bio=author_data.get("bio", ""),
                    profile_picture=author_data.get("profile_picture", None)
                )

                serialized_author = AuthorSerializer(instance=author).data
                return RepositoryResponse(True, serialized_author, "Author created successfully.")
        
        except IntegrityError as e:
            return RepositoryResponse(False, None, "Database Integrity Error: " + str(e))
        except Exception as e:
            return RepositoryResponse(False, None, "Error creating author: " + str(e))

    @staticmethod
    def get_author_by_id(author_id):
        try:
            author = Author.objects.filter(id=author_id).first()
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
                author = Author.objects.filter(id=author_id).first()
                if not author:
                    return RepositoryResponse(False, None, "Author not found.")

                if "email" in data:
                    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                    if not re.match(email_pattern, data["email"]):
                        return RepositoryResponse(False, None, "Invalid email format.")

                    if Author.objects.exclude(id=author_id).filter(user__email=data["email"]).exists():
                        return RepositoryResponse(False, None, "Email already exists.")

                if "username" in data and Author.objects.exclude(id=author_id).filter(user__username=data["username"]).exists():
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
    def delete_author(author_id):
        try:
            with transaction.atomic():
                author = Author.objects.filter(id=author_id).first()
                if not author:
                    return RepositoryResponse(False, None, "Author not found.")

                author.delete()
            return RepositoryResponse(True, None, "Author deleted successfully.")
        
        except Exception as e:
            return RepositoryResponse(False, None, "Error deleting author: " + str(e))
