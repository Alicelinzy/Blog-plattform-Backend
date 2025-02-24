from blog.models import Category
from django.db import IntegrityError
from rest_framework import status


class RepositoryResponse:
    def __init__(self, success: bool, data=None, message="", status_code=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.message = message
        self.status = status_code

    def __repr__(self):
        return f"RepositoryResponse(success={self.success}, data={self.data}, message={self.message}, status={self.status})"


class CategoryRepository:
    @staticmethod
    def format_category(category):
        """Helper function to format category data."""
        return {"id": category.id, "name": category.name} if category else None

    @staticmethod
    def create_category(name: str):
        try:
            if Category.objects.filter(name=name).exists():
                return RepositoryResponse(False, None, "Category with this name already exists.", status.HTTP_400_BAD_REQUEST)

            category = Category.objects.create(name=name)
            return RepositoryResponse(True, CategoryRepository.format_category(category), "Category created successfully.", status.HTTP_201_CREATED)
        except IntegrityError as e:
            return RepositoryResponse(False, None, f"Database integrity error: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return RepositoryResponse(False, None, f"Error creating category: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_category_by_id(category_id: int):
        try:
            category = Category.objects.filter(id=category_id).first()
            return RepositoryResponse(True, CategoryRepository.format_category(category), "Category found.", status.HTTP_200_OK) if category else RepositoryResponse(False, None, "Category not found.", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return RepositoryResponse(False, None, f"Error retrieving category: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_category_by_name(name: str):
        """New method to get a category by name."""
        try:
            category = Category.objects.filter(name=name).first()
            return RepositoryResponse(True, CategoryRepository.format_category(category), "Category found.", status.HTTP_200_OK) if category else RepositoryResponse(False, None, "Category not found.", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return RepositoryResponse(False, None, f"Error retrieving category: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_all_categories():
        try:
            categories = Category.objects.all()
            if categories.exists():
                formatted_categories = [CategoryRepository.format_category(cat) for cat in categories]
                return RepositoryResponse(True, formatted_categories, "Categories retrieved successfully.", status.HTTP_200_OK)
            return RepositoryResponse(False, None, "No categories found.", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return RepositoryResponse(False, None, f"Error retrieving categories: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def update_category(category_id: int, new_name: str):
        try:
            category = Category.objects.filter(id=category_id).first()
            if not category:
                return RepositoryResponse(False, None, "Category not found.", status.HTTP_404_NOT_FOUND)

            if Category.objects.exclude(id=category_id).filter(name=new_name).exists():
                return RepositoryResponse(False, None, "Another category with this name already exists.", status.HTTP_400_BAD_REQUEST)

            category.name = new_name
            category.save()
            return RepositoryResponse(True, CategoryRepository.format_category(category), "Category updated successfully.", status.HTTP_200_OK)
        except Exception as e:
            return RepositoryResponse(False, None, f"Error updating category: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete_category(category_id: int):
        try:
            category = Category.objects.filter(id=category_id).first()
            if not category:
                return RepositoryResponse(False, None, "Category not found.", status.HTTP_404_NOT_FOUND)

            category.delete()
            return RepositoryResponse(True, None, "Category deleted successfully.", status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return RepositoryResponse(False, None, f"Error deleting category: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
