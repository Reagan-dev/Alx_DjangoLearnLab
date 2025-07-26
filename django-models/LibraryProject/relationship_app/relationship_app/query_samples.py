import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian  # because of OneToOneField

if __name__ == "__main__":
    print("Books by George Orwell:")
    for book in books_by_author("George Orwell"):
        print(f"- {book.title}")

    print("\nBooks in Main Library:")
    for book in books_in_library("Main Library"):
        print(f"- {book.title}")

    librarian = librarian_for_library("Main Library")
    print(f"\nLibrarian of Main Library: {librarian.name}")