from rest_framework import serializers
from accounts.models import Author, Reader
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Author
        fields =  "__all__" 

class ReaderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Reader
        fields = "__all__" 