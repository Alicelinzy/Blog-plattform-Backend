from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import status  
import re

class ServiceResponse:
    def __init__(self, success: bool, data=None, message="", status=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.status = status

    def __str__(self):
        return f"(success={self.success}, data={self.data}, message={self.message}, status={self.status})"

class UserService:
    @staticmethod
    def create_user(user_data):
        try:
            with transaction.atomic():
                required_fields = ["username", "email"]
                for field in required_fields:
                    if field not in user_data or not user_data[field].strip(): 
                        return ServiceResponse(False, None, f"{field} is required.", status.HTTP_400_BAD_REQUEST)

                email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if not re.match(email_pattern, user_data["email"]):
                    return ServiceResponse(False, None, "Invalid email format.", status.HTTP_400_BAD_REQUEST)

                if User.objects.filter(username=user_data["username"]).exists():
                    return ServiceResponse(False, None, "Username already exists.", status.HTTP_400_BAD_REQUEST)

                if User.objects.filter(email=user_data["email"]).exists():
                    return ServiceResponse(False, None, "Email already exists.", status.HTTP_400_BAD_REQUEST)

                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    first_name=user_data.get("first_name", ""),
                    last_name=user_data.get("last_name", "")
                )
                if "password" in user_data:
                    user.set_password(user_data["password"])
                else:
                    return ServiceResponse(False, None, "Password is required.",  status.HTTP_400_BAD_REQUEST)

                user.save()
                return ServiceResponse(True, user, "User created successfully.", status.HTTP_201_CREATED)

        except IntegrityError as e:
            return ServiceResponse(False, None, f"Database error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return ServiceResponse(False, None, f"Error creating user: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
