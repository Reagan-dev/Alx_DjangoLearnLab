# advanced-api-project/advanced_api_project/api/serializers.py
# This file contains serializers for the Book and Author models.
# import necessary modules
from rest_framework import serializers
from .models import Book
from .models import Author
import datetime


# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation for the published year
    def validate_publication_year(self, value):
        # Ensure the publication year is not in the future
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer for books related to the author
    # This will include all books written by the author in the response
    books = BookSerializer(many=True, read_only=True, source='books')

    class Meta:
        # Specify the model and fields to be serialized
        model = Author  # Author model
        fields = ['id', 'name', 'books']  # Include books in the serialized output



