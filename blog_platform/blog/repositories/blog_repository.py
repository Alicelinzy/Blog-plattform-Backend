from blog.models import Blog, Category
from accounts.models import Author
from blog.serializers import BlogSerializer
from django.db import IntegrityError
from django.utils.timezone import now


class RepositoryResponse:
    def __init__(self, success: bool, data=None, message=""):
        self.success = success
        self.data = data
        self.message = message

    def __repr__(self):
        return f"RepositoryResponse(success={self.success}, data={self.data}, message={self.message})"


class BlogRepository:
    @staticmethod
    def create_blog(title: str, content: str, author_id: int, category_id: int = None, status: str = "draft"):
        try:
            author = Author.objects.filter(id=author_id).first()
            if not author:
                return RepositoryResponse(False, None, "Author not found.")

            category = Category.objects.filter(id=category_id).first() if category_id else None
            if category_id and not category:
                return RepositoryResponse(False, None, "Category not found.")

            if Blog.objects.filter(title=title).exists():
                return RepositoryResponse(False, None, "A blog with this title already exists.")

            blog = Blog.objects.create(
                title=title, content=content, author=author,
                category=category, status=status,
                published_at=now() if status == "published" else None
            )

            serialized_blog = BlogSerializer(blog).data
            return RepositoryResponse(True, serialized_blog, "Blog created successfully.")

        except IntegrityError as e:
            return RepositoryResponse(False, None, f"Database integrity error: {e}")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error creating blog: {e}")

    @staticmethod
    def get_blog_by_id(blog_id: int):
        blog = Blog.objects.filter(id=blog_id).first()
        if blog:
            serialized_blog = BlogSerializer(blog).data 
            return RepositoryResponse(True, serialized_blog, "Blog found.")
        return RepositoryResponse(False, None, "Blog not found.")

    @staticmethod
    def get_all_blogs():
        blogs = Blog.objects.all()
        if blogs.exists():
            serialized_blogs = BlogSerializer(blogs, many=True).data 
            return RepositoryResponse(True, serialized_blogs, "Blogs retrieved successfully.")
        return RepositoryResponse(False, None, "No blogs found.")

    @staticmethod
    def update_blog(blog_id: int, **update_data):
        try:
            blog = Blog.objects.filter(id=blog_id).first()
            if not blog:
                return RepositoryResponse(False, None, "Blog not found.")

            if "category_id" in update_data:
                category = Category.objects.filter(id=update_data["category_id"]).first()
                if not category:
                    return RepositoryResponse(False, None, "Category not found.")
                update_data["category"] = category
                del update_data["category_id"]

            if "author_id" in update_data:
                author = Author.objects.filter(id=update_data["author_id"]).first()
                if not author:
                    return RepositoryResponse(False, None, "Author not found.")
                update_data["author"] = author
                del update_data["author_id"]

            if "status" in update_data and update_data["status"] == "published":
                update_data["published_at"] = now()

            for key, value in update_data.items():
                setattr(blog, key, value)
            blog.save()

            serialized_blog = BlogSerializer(blog).data  
            return RepositoryResponse(True, serialized_blog, "Blog updated successfully.")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error updating blog: {e}")

    @staticmethod
    def delete_blog(blog_id: int):
        try:
            blog = Blog.objects.filter(id=blog_id).first()
            if not blog:
                return RepositoryResponse(False, None, "Blog not found.")

            blog.delete()
            return RepositoryResponse(True, None, "Blog deleted successfully.")
        except Exception as e:
            return RepositoryResponse(False, None, f"Error deleting blog: {e}")
