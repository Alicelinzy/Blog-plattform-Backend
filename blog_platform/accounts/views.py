from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.services.author_services import AuthorService
from accounts.services.reader_services import ReaderService
from accounts.models import Author, Reader

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = Author.objects.filter(user__username=username).first()
    user_type = "author"

    if not user:
        user = Reader.objects.filter(user__username=username).first()
        user_type = "reader"

    if not user or not check_password(password, user.user.password): 
        return Response({"success": False, "message": "Invalid credentials. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user.user)

    return Response({
        "success": True,
        "message": "Login successful!",
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "user": {
            "id": user.user.id,  
            "username": user.user.username,  
            "email": user.user.email,  
            "user_type": user_type
        }
    }, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_author(request):
    response = AuthorService.create_author(request.data)
    return Response({
        "success": response.success, 
        "message": response.message, 
        "data": response.data
    }, status=response.status)


@api_view(["POST"])
def create_reader(request):
    first_name = request.data.get("first_name")  
    last_name = request.data.get("last_name")  
    
    response = ReaderService.create_reader({
        "username": request.data.get("username"),
        "password": request.data.get("password"),
        "email": request.data.get("email"),
        "first_name": request.data.get("first_name"), 
        "last_name": request.data.get("last_name"), 
        "favorite_categories": request.data.get("favorite_categories", []),
    })

    return Response({
        "success": response.success, 
        "message": response.message, 
        "data": response.data
    }, status=response.status)

@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def get_all_authors(request):
    response = AuthorService.get_all_authors()

    if response.success:
        return Response({"success": True, "message": response.message, "data": response.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def get_author(request, author_id):
    response = AuthorService.get_author_by_id(author_id)

    if response.success:
        return Response({"success": True, "message": response.message, "data": response.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def get_all_readers(request):
    response = ReaderService.get_all_readers()

    if response.success:
        return Response({"success": True, "message": response.message, "data": response.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  
def get_reader(request, reader_id):
    response = ReaderService.get_reader_by_id(reader_id)

    if response.success:
        return Response({"success": True, "message": response.message, "data": response.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])  
def update_author(request, author_id):
    response = AuthorService.update_author(author_id, request.data)

    if response.success:
        return Response({"success": True, "message": response.message, "data": response.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])  
def update_reader(request, reader_id):
    response = ReaderService.update_reader(reader_id, request.data)

    if response.success:
        return Response({"success": True, "message": response.message, "data": response.data}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  
def delete_author(request, author_id):
    response = AuthorService.delete_author(author_id)

    if response.success:
        return Response({"success": True, "message": response.message}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  
def delete_reader(request, reader_id):
    response = ReaderService.delete_reader(reader_id)

    if response.success:
        return Response({"success": True, "message": response.message}, status=status.HTTP_200_OK)

    return Response({"success": False, "message": response.message}, status=status.HTTP_404_NOT_FOUND)