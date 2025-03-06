from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from blog.services.blog_services import BlogService
from blog.services.category_services import CategoryService
from blog.models import Blog

def is_author_or_admin(user, blog):
    """Allow authors to edit their own blogs and admins to manage all blogs."""
    return user.is_superuser or (user.is_authenticated and blog.author.user == user)



@api_view(["POST"])
@permission_classes([IsAuthenticated])  
def create_blog(request):
    user = request.user  
    title = request.data.get("title")
    content = request.data.get("content")
    category_id = request.data.get("category_id")

    response = BlogService.create_blog(user, title, content, category_id) 

    return Response({"success": response.success, "data": response.data, "message": response.message}, status=response.status)

@api_view(["GET"])
def get_blog(request, blog_id):
    """Retrieve a single blog post by ID. Readers can access it without authentication."""
    response = BlogService().get_blog_by_id(blog_id)
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_all_blogs(request):
    """Retrieve all blog posts. Readers can access them without authentication."""
    response = BlogService().get_all_blogs()
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["PUT", "PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def update_blog(request, blog_id):
    """Update an existing blog post. Authors can update their own blogs; admins can update all."""
    blog = Blog.objects.filter(id=blog_id).first()
    
    if not blog:
        return Response({"success": False, "message": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)

    if not is_author_or_admin(request.user, blog):
        return Response({"success": False, "message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    response = BlogService().update_blog(blog_id, **request.data)
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  
def delete_blog(request, blog_id):
    """Delete a blog post. Authors can delete their own blogs; admins can delete all."""
    blog = Blog.objects.filter(id=blog_id).first()
    
    if not blog:
        return Response({"success": False, "message": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)

    if not is_author_or_admin(request.user, blog):
        return Response({"success": False, "message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    response = BlogService().delete_blog(blog_id)
    return Response({"success": response.success, "message": response.message}, status=response.status)



@api_view(["POST"])
@permission_classes([IsAuthenticated])  
def create_category(request):
    """Create a new category."""
    response = CategoryService().create_category(request.data)
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_category(request, category_id):
    """Retrieve a category by ID. Publicly accessible."""
    response = CategoryService().get_category_by_id(category_id)
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_all_categories(request):
    """Retrieve all categories. Publicly accessible."""
    response = CategoryService().get_all_categories()
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])  
def update_category(request, category_id):
    """Update an existing category."""
    response = CategoryService().update_category(category_id, request.data)
    return Response({"success": response.success, "message": response.message, "data": response.data}, status=response.status)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  
def delete_category(request, category_id):
    """Delete a category."""
    response = CategoryService().delete_category(category_id)
    return Response({"success": response.success, "message": response.message}, status=response.status)
