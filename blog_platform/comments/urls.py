from django.urls import path
from comments.views import (
    create_comment, get_comment_by_id, get_all_comments,
    get_comments_by_blog, get_replies, update_comment, delete_comment
)

urlpatterns = [
    path("", create_comment, name="create_comment"),
    path("<int:comment_id>/", get_comment_by_id, name="get_comment"),
    path("all/", get_all_comments, name="get_all_comments"),
    path("blog/<int:blog_id>/", get_comments_by_blog, name="get_comments_by_blog"),
    path("replies/<int:parent_comment_id>/", get_replies, name="get_replies"),
    path("<int:comment_id>/update/", update_comment, name="update_comment"),
    path("<int:comment_id>/delete/", delete_comment, name="delete_comment"),
]
