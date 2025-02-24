from blog.repositories.category_repository import CategoryRepository
from blog.serializers import CategorySerializer 
from base.utils.responses import APIResponse
from rest_framework import status


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()

    def get_all_categories(self):
        response = self.category_repo.get_all_categories()
        if not response.success:
            return APIResponse(False, None, "Failed to fetch categories.", status=status.HTTP_404_NOT_FOUND)

        serialized_data = CategorySerializer(response.data, many=True).data
        return APIResponse(True, serialized_data, "Categories retrieved successfully.", status=status.HTTP_200_OK)

    def get_category_by_id(self, category_id):
        response = self.category_repo.get_category_by_id(category_id)
        if not response.success:
            return APIResponse(False, None, f"Category with ID {category_id} not found.", status=status.HTTP_404_NOT_FOUND)

        serialized_data = CategorySerializer(response.data).data
        return APIResponse(True, serialized_data, "Category retrieved successfully.", status=status.HTTP_200_OK)

    def create_category(self, data):
        """Creates a new category if the name is unique."""
        category_name = data.get("name")
        if not category_name:
            return APIResponse(False, None, "Category name is required.", status=status.HTTP_400_BAD_REQUEST)

        existing_category = self.category_repo.get_category_by_name(category_name)
        if existing_category.success:
            return APIResponse(False, None, "Category with this name already exists.", status=status.HTTP_400_BAD_REQUEST)

        response = self.category_repo.create_category(category_name)
        if not response.success:
            return APIResponse(False, None, "Failed to create category.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serialized_data = CategorySerializer(response.data).data
        return APIResponse(True, serialized_data, "Category created successfully.", status=status.HTTP_201_CREATED)

    def update_category(self, category_id, data):
        """Updates an existing category."""
        category_name = data.get("name")
        if not category_name:
            return APIResponse(False, None, "Category name is required.", status=status.HTTP_400_BAD_REQUEST)

        existing_category = self.category_repo.get_category_by_id(category_id)
        if not existing_category.success:
            return APIResponse(False, None, f"Category with ID {category_id} not found.", status=status.HTTP_404_NOT_FOUND)

        response = self.category_repo.update_category(category_id, category_name)
        if not response.success:
            return APIResponse(False, None, "Failed to update category.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serialized_data = CategorySerializer(response.data).data
        return APIResponse(True, serialized_data, "Category updated successfully.", status=status.HTTP_200_OK)

    def delete_category(self, category_id):
        """Deletes an existing category."""
        response = self.category_repo.delete_category(category_id)
        if not response.success:
            return APIResponse(False, None, f"Failed to delete category: {response.message}", status=response.status)
        return APIResponse(True, None, "Category deleted successfully.", status=status.HTTP_204_NO_CONTENT)
