from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from .models import Article
from .models import Book
from .forms import ExampleForm

# View to list all books, protected by can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_article(request):
    # Code for creating article (form logic here)
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_article(request, article_id):
    # Code for editing article
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_article(request, article_id):
    # Code for deleting article
    pass

# Example of searching books by user input inside a view function
def search_books(request):
    user_input = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=user_input)
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Example of handling BookForm inside a view function
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

def example_form_view(request):
    form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})