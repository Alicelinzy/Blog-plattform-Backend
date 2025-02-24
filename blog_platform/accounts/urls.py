from django.urls import path
from accounts.views import (
    create_author, create_reader, get_all_authors,
    get_all_readers, update_user, delete_user, login_view
)

urlpatterns = [
    path("login/", login_view, name="custom-login"),
    path("authors/create/", create_author, name="create-author"), 
    path("readers/create/", create_reader, name="create_reader"),
    path("authors/", get_all_authors, name="get_all_authors"),
    path("readers/", get_all_readers, name="get_all_readers"),
    path("users/update/<int:user_id>/", update_user, name="update_user"),
    path("users/delete/<int:user_id>/", delete_user, name="delete_user"),
]
