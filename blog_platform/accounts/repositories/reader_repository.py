from accounts.models import Reader
from blog.models import Category  
from django.db import transaction
from django.db import transaction, IntegrityError

class RepositoryResponse:
    def __init__(self, success: bool, data=None, message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return f"(success={self.success}, data={self.data}, message={self.message})"

class ReaderRepository:
    @staticmethod
    def create_reader(user, favorite_categories=None):
        try:
            with transaction.atomic():
                """Check if reader already exists"""
                if Reader.objects.filter(user=user).exists():
                    return RepositoryResponse(False, None, "Reader already exists for this user.")

                """Create Reader"""
                reader = Reader.objects.create(user=user)

                """Assign favorite categories if provided"""
                if favorite_categories:
                    categories = Category.objects.filter(id__in=favorite_categories) 
                    reader.favorite_categories.set(categories)

                return RepositoryResponse(True, reader, "Reader created successfully")

        except IntegrityError as e:
            return RepositoryResponse(False, None, "Database Integrity Error: " + str(e))

        except Exception as e:
            return RepositoryResponse(False, None, "Error creating reader: " + str(e))

    @staticmethod
    def get_reader_by_id(reader_id):
        try:
            reader = Reader.objects.prefetch_related("favorite_categories").get(id=reader_id)
            return RepositoryResponse(True, reader, "Reader found")
        except Reader.DoesNotExist:
            return RepositoryResponse(False, None, "Reader not found")

    @staticmethod
    def get_all_readers():
        try:
            readers = Reader.objects.prefetch_related("favorite_categories").all()
            return RepositoryResponse(True, readers, "Readers retrieved successfully")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error retrieving readers: {str(e)}")

    @staticmethod
    def update_reader(reader_id, data):
        try:
            reader = Reader.objects.get(id=reader_id)
            if "favorite_categories" in data:
                categories = Category.objects.filter(id__in=data["favorite_categories"])
                reader.favorite_categories.set(categories)
            reader.save()
            return RepositoryResponse(True, reader, "Reader updated successfully")
        except Reader.DoesNotExist:
            return RepositoryResponse(False, None, "Reader not found")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error updating reader: {str(e)}")

    @staticmethod
    def delete_reader(reader_id):
        try:
            reader = Reader.objects.get(id=reader_id)
            reader.delete()
            return RepositoryResponse(True, None, "Reader deleted successfully")
        except Reader.DoesNotExist:
            return RepositoryResponse(False, None, "Reader not found")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error deleting reader: {str(e)}")
