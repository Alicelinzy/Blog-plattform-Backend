from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from blog.services.blog_services import BlogService
from blog.services.category_services import CategoryService

blog_service = BlogService()
category_service = CategoryService()

@api_view(["POST"])
def create_blog(request):
    """
    Create a new blog post.
    """
    data = request.data
    response = blog_service.create_blog(
        title=data.get("title"),
        content=data.get("content"),
        author_id=data.get("author_id"),
        category_id=data.get("category_id"),
    )
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_blog(request, blog_id):
    """Retrieve a single blog post by ID."""
    response = blog_service.get_blog_by_id(blog_id)
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_all_blogs(request):
    """ Retrieve all blog posts."""
    response = blog_service.get_all_blogs()
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["PUT", "PATCH"])
def update_blog(request, blog_id):
    """ Update an existing blog post. """
    response = blog_service.update_blog(blog_id, **request.data)
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["DELETE"])
def delete_blog(request, blog_id):
    """Delete a blog post."""
    response = blog_service.delete_blog(blog_id)
    return Response({"message": response.message}, status=response.status)

@api_view(["POST"])
def create_category(request):
    """Create a new category."""
    response = category_service.create_category(request.data)
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_category(request, category_id):
    """ Retrieve a category by ID. """
    response = category_service.get_category_by_id(category_id)
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["GET"])
def get_all_categories(request):
    """Retrieve all categories. """
    response = category_service.get_all_categories()
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["PUT", "PATCH"])
def update_category(request, category_id):
    """Update an existing category. """
    response = category_service.update_category(category_id, request.data)
    return Response({"message": response.message, "data": response.data}, status=response.status)

@api_view(["DELETE"])
def delete_category(request, category_id):
    """Delete a category. """
    response = category_service.delete_category(category_id)
    return Response({"message": response.message}, status=response.status)

