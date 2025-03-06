from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from blog.models import Blog, Category
from accounts.models import Author
from django.contrib.auth.models import User

class BlogCategoryTests(APITestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Tech")
        self.user = User.objects.create_user(username="author", password="testpassword", email="author@example.com")
        self.author = Author.objects.create(user=self.user)
        self.token = RefreshToken.for_user(self.author.user).access_token

        self.blog = Blog.objects.create(
            title="Sample Blog",
            content="This is a test blog content",
            author=self.author,
            category=self.category
        )

    # ----------- Helper Methods -----------
    def authenticate(self):
        """Helper method to authenticate the client."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # ----------- Blog CRUD Tests -----------    
    def test_create_blog(self):
        url = reverse('create_blog')
        data = {
            "title": "New Blog",
            "content": "This is a new blog",
            "category_id": self.category.id
        }
        self.authenticate()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)  

    def test_get_blog(self):
        url = reverse('get_blog', args=[self.blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], self.blog.title)

    def test_get_all_blogs(self):
        url = reverse('get_all_blogs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)  
    def test_update_blog(self):
        url = reverse('update_blog', args=[self.blog.id])
        data = {
            "title": "Updated Blog",
            "content": "This is the updated content of the blog"
        }
        self.authenticate()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Updated Blog")

    def test_delete_blog(self):
        url = reverse('delete_blog', args=[self.blog.id])
        self.authenticate()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Blog.objects.count(), 0) 

    def test_create_blog_without_authentication(self):
        url = reverse('create_blog')
        data = {
            "title": "Unauthorized Blog",
            "content": "Content without authorization",
            "category_id": self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # # ----------- Category CRUD Tests -----------    
    def test_create_category(self):
        url = reverse('create_category')
        data = {"name": "Science"}
        self.authenticate()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  

    def test_get_category(self):
        url = reverse('get_category', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.category.name)

    def test_get_all_categories(self):
        url = reverse('get_all_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)  

    def test_update_category(self):
        url = reverse('update_category', args=[self.category.id])
        data = {"name": "Updated Science"}
        self.authenticate()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Science")

    def test_delete_category(self):
        url = reverse('delete_category', args=[self.category.id])
        self.authenticate()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)  

    def test_create_category_without_authentication(self):
        url = reverse('create_category')
        data = {"name": "Unauthorized Category"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # # ----------- Edge Cases and Additional Tests -----------
    def test_update_blog_with_invalid_data(self):
        url = reverse('update_blog', args=[self.blog.id])
        data = {
            "title": "",  
            "content": "This is the updated content of the blog"
        }
        self.authenticate()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_nonexistent_blog(self):
        url = reverse('delete_blog', args=[999])  
        self.authenticate()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nonexistent_category(self):
        url = reverse('get_category', args=[999])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)