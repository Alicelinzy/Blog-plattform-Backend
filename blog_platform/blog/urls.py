from django.urls import path
from blog.views import (
    create_blog, get_blog, get_all_blogs, update_blog,  delete_blog, create_category, get_category, 
    get_all_categories, update_category, delete_category,
)

urlpatterns = [
    # Blog endpoints
    path("blogs/", create_blog, name="create_blog"),  
    path("blogs/<int:blog_id>/", get_blog, name="get_blog"), 
    path("blogs/all/", get_all_blogs, name="get_all_blogs"),  
    path("blogs/<int:blog_id>/update/", update_blog, name="update_blog"),  
    path("blogs/<int:blog_id>/delete/", delete_blog, name="delete_blog"), 

    # Category endpoints
    path("categories/", create_category, name="create_category"), 
    path("categories/<int:category_id>/", get_category, name="get_category"),  
    path("categories/all/", get_all_categories, name="get_all_categories"), 
    path("categories/<int:category_id>/update/", update_category, name="update_category"), 
    path("categories/<int:category_id>/delete/", delete_category, name="delete_category"), 
]