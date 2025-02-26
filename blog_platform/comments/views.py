from rest_framework.decorators import api_view
from rest_framework.response import Response
from comments.services.comment_services import CommentService


@api_view(['POST'])
def create_comment(request):
    response = CommentService.create_comment(request.data)
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response(response.data if response.data else {}, status=response.status)


@api_view(['GET'])
def get_comment_by_id(request, comment_id):
    response = CommentService.get_comment_by_id(comment_id)
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response(response.data if response.data else {}, status=response.status)


@api_view(['GET'])
def get_all_comments(request):
    response = CommentService.get_all_comments()
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response(response.data if response.data else {}, status=response.status)


@api_view(['GET'])
def get_comments_by_blog(request, blog_id):
    response = CommentService.get_comments_by_blog(blog_id)
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response(response.data if response.data else {}, status=response.status)


@api_view(['GET'])
def get_replies(request, parent_comment_id):
    response = CommentService.get_replies(parent_comment_id)
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response(response.data if response.data else {}, status=response.status)


@api_view(['PUT', 'PATCH'])
def update_comment(request, comment_id):
    response = CommentService.update_comment(comment_id, request.data)
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response(response.data if response.data else {}, status=response.status)


@api_view(['DELETE'])
def delete_comment(request, comment_id):
    response = CommentService.delete_comment(comment_id)
    if not response.success:
        return Response({"message": response.message}, status=response.status)
    return Response({"message": response.message}, status=response.status)
