from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from accounts.services.author_services import AuthorService
from accounts.services.reader_services import ReaderService
from accounts.models import Author, Reader


@api_view(["POST"])
def create_author(request):
    print("Received data:", request.data)  

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    response = AuthorService.create_author(request.data)
    
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)


@api_view(["POST"])
def create_reader(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    favorite_categories = request.data.get("favorite_categories", [])

    response = ReaderService.create_reader({
        "username": username,
        "password": password,
        "email": email,
        "favorite_categories": favorite_categories,
    })

    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def get_all_authors(request):
    response = AuthorService.get_all_authors()
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)


@api_view(["GET"])
@permission_classes([IsAuthenticated]) 
def get_all_readers(request):
    response = ReaderService.get_all_readers()
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated]) 
def update_user(request, user_id):
    response = AuthorService.update_author(user_id, **request.data)

    if not response.success:  
        response = ReaderService.update_reader(user_id, **request.data)  

    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  
def delete_user(request, user_id):
    author_response = AuthorService.delete_author(user_id)

    if author_response.message == "Author not found":
        response = ReaderService.delete_reader(user_id)
    else:
        response = author_response

    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # Try to find the user in Author and Reader models
    user = Author.objects.filter(username=username).first()
    user_type = "author"

    if not user:
        user = Reader.objects.filter(username=username).first()
        user_type = "reader"

    if not user or not check_password(password, user.password):  
        return Response({"success": False, "message": "Invalid credentials. Please try again."},
                        status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT tokens manually
    access_token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=4), 
        "user_type": user_type
    }
    
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=14),  
    }

    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")

    return Response({
        "success": True,
        "message": "Login successful!",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user_type
        }
    }, status=status.HTTP_200_OK) 
