from .views import BookList
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from django.urls import include
# Create a router and register our viewset with it.

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')
urlpatterns = router.urls

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
    path('', include(router.urls))  # Include the router URLs
]