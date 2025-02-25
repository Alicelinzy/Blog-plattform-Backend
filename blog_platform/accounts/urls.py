from django.urls import path
from accounts.views import (
    create_author, create_reader, get_all_authors, get_author,
    get_all_readers, get_reader, update_author, update_reader,
    delete_author, delete_reader, login_view
)

urlpatterns = [
    path("login/", login_view, name="custom-login"),
    
    path("authors/create/", create_author, name="create-author"), 
    path("authors/", get_all_authors, name="get_all_authors"),
    path("authors/<int:author_id>/", get_author, name="get_author"),
    path("authors/update/<int:author_id>/", update_author, name="update_author"),
    path("authors/delete/<int:author_id>/", delete_author, name="delete_author"),
    
    path("readers/create/", create_reader, name="create_reader"),
    path("readers/", get_all_readers, name="get_all_readers"),
    path("readers/<int:reader_id>/", get_reader, name="get_reader"),
    path("readers/update/<int:reader_id>/", update_reader, name="update_reader"),
    path("readers/delete/<int:reader_id>/", delete_reader, name="delete_reader"),
]
