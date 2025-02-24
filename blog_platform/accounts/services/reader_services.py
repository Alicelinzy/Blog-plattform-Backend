import re
from django.db import transaction
from rest_framework import status
from accounts.repositories.reader_repository import ReaderRepository
from accounts.serializers import ReaderSerializer
from accounts.services.user_serivces import UserService, ServiceResponse


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
    def create_reader(data):
        try:
            with transaction.atomic():
                user_fields = ["username", "password", "email", "first_name", "last_name"]
                user_data = {field: data.get(field, "").strip() for field in user_fields}
                favorite_categories = data.get("favorite_categories", [])

                user_response = UserService.create_user(user_data)
                if not user_response.success:
                    return ServiceResponse(False, None, user_response.message, user_response.status)

                user = user_response.data  
                reader_response = ReaderRepository.create_reader(user, favorite_categories)
                
                if not reader_response.success:
                    return ServiceResponse(False, None, reader_response.message, status.HTTP_400_BAD_REQUEST)

                serialized_reader = ReaderSerializer(reader_response.data).data
                return ServiceResponse(True, serialized_reader, "Reader created successfully", status.HTTP_201_CREATED)
        
        except Exception as e:
            return ServiceResponse(False, None, f"Error creating reader: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_reader_by_id(reader_id: int):
        response = ReaderRepository.get_reader_by_id(reader_id)
        if response.success:
            reader = response.data
            user = reader.user
            reader_data = {
                "id": reader.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "favorite_categories": list(reader.favorite_categories.values_list("name", flat=True)),  
                "created_at": reader.created_at,
            }
            return APIResponse(True, reader_data, response.message, status.HTTP_200_OK)

        return APIResponse(False, None, response.message, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_all_readers():
        response = ReaderRepository.get_all_readers()

        if response.success:
            serialized_readers = ReaderSerializer(response.data, many=True).data 
            return APIResponse(True, serialized_readers, response.message, status.HTTP_200_OK)

        return APIResponse(False, None, response.message, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_reader(reader_id: int, data):
        if not data:
            return APIResponse(False, None, "No fields provided to update", status.HTTP_400_BAD_REQUEST)

        response = ReaderRepository.get_reader_by_id(reader_id)
        if not response.success:
            return APIResponse(False, None, "Reader not found", status.HTTP_404_NOT_FOUND)

        reader = response.data
        user = reader.user

        user_fields = ["username", "email", "first_name", "last_name"]
        user_data = {key: data[key] for key in user_fields if key in data}
        reader_data = {"favorite_categories": data.get("favorite_categories")} if "favorite_categories" in data else {}

        with transaction.atomic():
            if user_data:
                user_response = UserService.update_user(user.id, user_data)
                if not user_response.success:
                    return APIResponse(False, None, user_response.message, user_response.status)

            if reader_data:
                reader_response = ReaderRepository.update_reader(reader_id, reader_data)
                if not reader_response.success:
                    return APIResponse(False, None, reader_response.message, status.HTTP_400_BAD_REQUEST)

        updated_reader = ReaderRepository.get_reader_by_id(reader_id).data
        return APIResponse(True, ReaderSerializer(updated_reader).data, "Reader updated successfully", status.HTTP_200_OK)

    @staticmethod
    def delete_reader(reader_id: int):
        response = ReaderRepository.get_reader_by_id(reader_id)
        if not response.success:
            return APIResponse(False, None, "Reader not found", status.HTTP_404_NOT_FOUND)

        reader = response.data
        user_id = reader.user.id  
        with transaction.atomic():
            reader_response = ReaderRepository.delete_reader(reader_id)
            if not reader_response.success:
                return APIResponse(False, None, reader_response.message, status.HTTP_400_BAD_REQUEST)

            user_response = UserService.delete_user(user_id)
            if not user_response.success:
                return APIResponse(False, None, user_response.message, user_response.status)

        return APIResponse(True, None, "Reader deleted successfully", status.HTTP_200_OK)
