from rest_framework import serializers
from accounts.models import Author, Reader

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields =  "__all__" 

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = "__all__" 