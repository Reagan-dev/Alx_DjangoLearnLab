from django.db import models

# Create your models here.
# This file contains the Book and Author models for the API project.
# Author model
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.namex


# This model represents a book with a title, author, and publication year.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_year = models.IntegerField()

    def __str__(self):
        return self.title

