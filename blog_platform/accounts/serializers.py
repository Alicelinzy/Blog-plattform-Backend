from rest_framework import serializers
from accounts.models import Author, Reader

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "username", "first_name", "last_name", "email", "bio", "date_joined"]

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ["id", "username", "first_name", "last_name", "email","is_staff", "date_joined"]
