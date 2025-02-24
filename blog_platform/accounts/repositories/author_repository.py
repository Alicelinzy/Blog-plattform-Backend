from accounts.models import Author
from accounts.serializers import AuthorSerializer 
from django.db import IntegrityError, transaction
import re


class RepositoryResponse:
    def __init__(self, success: bool, data=None, message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return f"(success={self.success}, data={self.data}, message={self.message})"


class AuthorRepository:
    @staticmethod
    def create_author(data):
        try:
            with transaction.atomic():
                required_fields = ["username", "email", "password"]
                for field in required_fields:
                    if field not in data or not data[field].strip():
                        return RepositoryResponse(False, None, f"{field} is required.")

                email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if not re.match(email_pattern, data["email"]):
                    return RepositoryResponse(False, None, "Invalid email format.")

                if Author.objects.filter(username=data["username"]).exists():
                    return RepositoryResponse(False, None, "Username already exists.")
                if Author.objects.filter(email=data["email"]).exists():
                    return RepositoryResponse(False, None, "Email already exists.")

                author = Author.objects.create_user(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"],
                )

                # We will Use serializer to return structured data
                serialized_author = AuthorSerializer(author)
                return RepositoryResponse(True, serialized_author.data, "Author created successfully.")

        except IntegrityError as e:
            return RepositoryResponse(False, None, "Database integrity error: " + str(e))
        except Exception as e:
            return RepositoryResponse(False, None, "Error creating author: " + str(e))

    @staticmethod
    def get_author_by_id(author_id):
        try:
            author = Author.objects.filter(id=author_id).first()
            if author:
                serialized_author = AuthorSerializer(author)
                return RepositoryResponse(True, serialized_author.data, "Author found.")
            return RepositoryResponse(False, None, "Author not found.")
        except Exception as e:
            return RepositoryResponse(False, None, "Error retrieving author: " + str(e))

    @staticmethod
    def get_all_authors():
        try:
            authors = Author.objects.all()
            serialized_authors = AuthorSerializer(authors, many=True)
            return RepositoryResponse(True, serialized_authors.data, "Authors retrieved successfully.")
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

                    if Author.objects.exclude(id=author_id).filter(email=data["email"]).exists():
                        return RepositoryResponse(False, None, "Email already exists.")

                if "username" in data and Author.objects.exclude(id=author_id).filter(username=data["username"]).exists():
                    return RepositoryResponse(False, None, "Username already exists.")

                for key, value in data.items():
                    setattr(author, key, value)
                author.save()

                serialized_author = AuthorSerializer(author)
                return RepositoryResponse(True, serialized_author.data, "Author updated successfully.")

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
