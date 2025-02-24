import re
from django.db import IntegrityError, transaction
from accounts.models import Reader
from accounts.serializers import ReaderSerializer


class RepositoryResponse:
    def __init__(self, success: bool, data=None, message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return f"(success={self.success}, data={self.data}, message={self.message})"


class ReaderRepository:
    @staticmethod
    def create_reader(data):
        """Creates a new reader with validation checks."""
        try:
            with transaction.atomic():
                required_fields = ["username", "email", "password"]
                for field in required_fields:
                    if not data.get(field) or not data[field].strip():
                        return RepositoryResponse(False, None, f"{field} is required.")

                email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if not re.match(email_regex, data["email"]):
                    return RepositoryResponse(False, None, "Invalid email format.")


                if Reader.objects.filter(username=data["username"]).exists():
                    return RepositoryResponse(False, None, "Username is already taken.")
                if Reader.objects.filter(email=data["email"]).exists():
                    return RepositoryResponse(False, None, "Email is already in use.")

                if len(data["password"]) < 8:
                    return RepositoryResponse(False, None, "Password must be at least 8 characters long.")

                reader = Reader(username=data["username"], email=data["email"])
                reader.set_password(data["password"])
                reader.save()

                return RepositoryResponse(True, ReaderSerializer(reader).data, "Reader created successfully.")

        except IntegrityError as e:
            return RepositoryResponse(False, None, f"Database integrity error: {str(e)}")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error creating reader: {str(e)}")

    @staticmethod
    def get_reader_by_id(reader_id):
        """Fetches a reader by ID."""
        try:
            reader = Reader.objects.filter(id=reader_id).first()
            if reader:
                return RepositoryResponse(True, ReaderSerializer(reader).data, "Reader found.")
            return RepositoryResponse(False, None, "Reader not found.")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error retrieving reader: {str(e)}")

    @staticmethod
    def get_all_readers():
        """Retrieves all readers."""
        try:
            readers = Reader.objects.all()
            return RepositoryResponse(True, ReaderSerializer(readers, many=True).data, "Readers retrieved successfully.")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error retrieving readers: {str(e)}")

    @staticmethod
    def update_reader(reader_id, data):
        """Updates a reader's details."""
        try:
            with transaction.atomic():
                reader = Reader.objects.filter(id=reader_id).first()
                if not reader:
                    return RepositoryResponse(False, None, "Reader not found.")

                if "email" in data:
                    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                    if not re.match(email_regex, data["email"]):
                        return RepositoryResponse(False, None, "Invalid email format.")

                    if Reader.objects.exclude(id=reader_id).filter(email=data["email"]).exists():
                        return RepositoryResponse(False, None, "Email is already in use.")
                for key, value in data.items():
                    setattr(reader, key, value)
                reader.save()

                return RepositoryResponse(True, ReaderSerializer(reader).data, "Reader updated successfully.")

        except Exception as e:
            return RepositoryResponse(False, None, f"Error updating reader: {str(e)}")

    @staticmethod
    def delete_reader(reader_id):
        """Deletes a reader."""
        try:
            with transaction.atomic():
                reader = Reader.objects.filter(id=reader_id).first()
                if not reader:
                    return RepositoryResponse(False, None, "Reader not found.")

                reader.delete()
                return RepositoryResponse(True, None, "Reader deleted successfully.")

        except Exception as e:
            return RepositoryResponse(False, None, f"Error deleting reader: {str(e)}")
