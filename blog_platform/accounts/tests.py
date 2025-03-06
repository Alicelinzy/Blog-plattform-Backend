from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from accounts.models import Author, Reader
from rest_framework_simplejwt.tokens import RefreshToken


class LoginTestCase(APITestCase):
    def setUp(self):
        """Set up a test user before each test."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.author = Author.objects.create(user=self.user)
        self.login_url = reverse("custom-login")

    def test_login_successful(self):
        """Test if a user can log in with correct credentials."""
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access_token" in response.data)
        self.assertTrue("refresh_token" in response.data)
        self.assertEqual(response.data["user"]["username"], "testuser")

    def test_login_invalid_credentials(self):
        """Test login with incorrect password."""
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Invalid credentials. Please try again.")

    def test_login_non_existent_user(self):
        """Test login with a user that doesn't exist."""
        data = {"username": "nonexistent", "password": "testpassword"}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Invalid credentials. Please try again.")


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test class."""
        cls.author_user = User.objects.create_user(
            username="author1", password="password123", email="author1@example.com"
        )
        cls.author = Author.objects.create(user=cls.author_user)

        cls.reader_user = User.objects.create_user(
            username="reader1", password="password123", email="reader1@example.com"
        )
        cls.reader = Reader.objects.create(user=cls.reader_user)

        # Generate JWT token
        refresh = RefreshToken.for_user(cls.author_user)
        cls.access_token = str(refresh.access_token)

        # Authentication headers
        cls.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {cls.access_token}"}

    def test_create_author(self):
        """Test creating an author (admin-only)."""
        url = reverse("create_author")
        data = {
            "username": "new_author",
            "password": "password123",
            "email": "new_author@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertTrue(Author.objects.filter(user__username="new_author").exists())

    def test_create_reader(self):
        """Test creating a reader."""
        url = reverse("create_reader")
        data = {
            "username": "new_reader",
            "password": "password123",
            "email": "new_reader@example.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "favorite_categories": [],
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertTrue(Reader.objects.filter(user__username="new_reader").exists())

    def test_get_all_authors(self):
        """Test retrieving all authors (requires authentication)."""
        url = reverse("get_all_authors")
        response = self.client.get(url, **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_author(self):
        """Test retrieving a specific author."""
        url = reverse("get_author", args=[self.author.id])
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_author(self):
        """Test updating an author profile (self-update only)."""
        url = reverse("update_author", args=[self.author.id])
        data = {"first_name": "UpdatedName"}

        response = self.client.put(url, data, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.user.first_name, "UpdatedName")

    def test_delete_author(self):
        """Test deleting an author (self-deletion only)."""
        url = reverse("delete_author", args=[self.author.id])

        response = self.client.delete(url, **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())

    def test_get_all_readers(self):
        """Test retrieving all readers."""
        url = reverse("get_all_readers")
        response = self.client.get(url, **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_reader(self):
        """Test retrieving a specific reader."""
        url = reverse("get_reader", args=[self.reader.id])
        response = self.client.get(url, **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["username"], self.reader.user.username)  # Updated assertion

    def test_update_reader(self):
        """Test updating a reader profile (self-update only)."""
        url = reverse("update_reader", args=[self.reader.id])
        data = {"first_name": "UpdatedReader"}

        response = self.client.put(url, data, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reader.refresh_from_db()
        self.assertEqual(self.reader.user.first_name, "UpdatedReader")

    def test_delete_reader(self):
        """Test deleting a reader (self-deletion only)."""
        url = reverse("delete_reader", args=[self.reader.id])
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reader.objects.filter(id=self.reader.id).exists())