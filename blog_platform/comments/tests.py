from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from blog.models import Blog
from accounts.models import Author, Reader
from comments.models import Comment
from django.contrib.auth.models import User  


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.author = Author.objects.create(user=self.user, bio="Test Author")
        self.blog = Blog.objects.create(
            title="Test Blog",
            content="Test Content",
            author=self.author  
        )
        self.reader = Reader.objects.create(user_id=self.user.id)  
        self.comment = Comment.objects.create(
            blog=self.blog,
            author=self.author,
            content="Test Comment"
        )

    # ----------- Create Comment Tests -----------
    def test_create_comment(self):
        url = reverse('create_comment')
        data = {
            "blog_id": self.blog.id,
            "author_id": self.author.id,
            "content": "New Comment"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_comment_missing_fields(self):
        url = reverse('create_comment')
        data = {
            "blog_id": self.blog.id,
            "content": "New Comment"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # # ----------- Retrieve Comment Tests -----------
    def test_get_comment_by_id(self):
        url = reverse('get_comment', args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.comment.content)

    def test_get_nonexistent_comment(self):
        url = reverse('get_comment', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # # ----------- Update Comment Tests -----------
    def test_update_comment(self):
        url = reverse('update_comment', args=[self.comment.id])
        data = {
            "content": "Updated Comment"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Updated Comment")

    def test_update_nonexistent_comment(self):
        url = reverse('update_comment', args=[999])
        data = {
            "content": "Updated Comment"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # # ----------- Delete Comment Tests -----------
    def test_delete_comment(self):
        url = reverse('delete_comment', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_nonexistent_comment(self):
        url = reverse('delete_comment', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)