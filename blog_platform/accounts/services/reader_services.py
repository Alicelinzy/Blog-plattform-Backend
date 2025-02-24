import re
from django.db import transaction
from rest_framework import status
from accounts.repositories.reader_repository import ReaderRepository
from accounts.serializers import ReaderSerializer


class APIResponse:
    def __init__(self, success: bool, data=None, message="", status=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.status = status

    def __str__(self):
        return f"APIResponse(success={self.success}, data={self.data}, message={self.message}, status={self.status})"


class ReaderService:
    @staticmethod
    def validate_email(email):
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    @staticmethod
    def create_reader(username: str, password: str, email: str):
        if not all([username, password, email]):
            return APIResponse(False, None, "All fields are required", status.HTTP_400_BAD_REQUEST)

        if not ReaderService.validate_email(email):
            return APIResponse(False, None, "Invalid email format", status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return APIResponse(False, None, "Password must be at least 8 characters", status.HTTP_400_BAD_REQUEST)

        response = ReaderRepository.create_reader({"username": username, "password": password, "email": email})

        if response.success:
            serialized_reader = ReaderSerializer(response.data).data
        else:
            serialized_reader = None

        return APIResponse(response.success, serialized_reader, response.message,status.HTTP_201_CREATED if response.success else status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_reader_by_id(reader_id: int):
        response = ReaderRepository.get_reader_by_id(reader_id)

        if response.success:
            serialized_reader = ReaderSerializer(response.data).data 
            return APIResponse(True, serialized_reader, response.message, status.HTTP_200_OK)

        return APIResponse(False, None, response.message, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_all_readers():
        response = ReaderRepository.get_all_readers()

        if response.success:
            serialized_readers = ReaderSerializer(response.data, many=True).data 
            return APIResponse(True, serialized_readers, response.message, status.HTTP_200_OK)

        return APIResponse(False, None, response.message, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_reader(reader_id: int, **kwargs):
        if not kwargs:
            return APIResponse(False, None, "No fields provided to update", status.HTTP_400_BAD_REQUEST)

        response = ReaderRepository.get_reader_by_id(reader_id)
        if not response.success:
            return APIResponse(False, None, "Reader not found", status.HTTP_404_NOT_FOUND)

        if "email" in kwargs and not ReaderService.validate_email(kwargs["email"]):
            return APIResponse(False, None, "Invalid email format", status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            response = ReaderRepository.update_reader(reader_id, kwargs)

        if response.success:
            serialized_reader = ReaderSerializer(response.data).data 
            return APIResponse(True, serialized_reader, response.message, status.HTTP_200_OK)

        return APIResponse(False, None, response.message, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_reader(reader_id: int):
        response = ReaderRepository.get_reader_by_id(reader_id)
        if not response.success:
            return APIResponse(False, None, "Reader not found", status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            response = ReaderRepository.delete_reader(reader_id)

        return APIResponse(response.success, None, response.message, status.HTTP_200_OK if response.success else status.HTTP_400_BAD_REQUEST)
