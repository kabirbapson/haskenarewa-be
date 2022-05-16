from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path

from books.models import UserReadingList
from books.views import getBookNow
from .api import BookAPI, BuyBookAPI, CategoryViewSet, GetBookGenreAPI, PublishBookAPI, ReadBookAPI, GetBooksViewSet,  GetTrendingBillBoardViewSet, LikeAPI, SearchAPI, UpdateBookTypeAPI, UploadPdfBookAPI, UserBookAPI, UserLibraryAPI, UserReadingListViewSet,  generateHomeAPI, getBookContentAPI

router = SimpleRouter()
# router.register('', BookAPI)
router.register(r'library', BookAPI, basename='library')
router.register(r'home', CategoryViewSet, basename='categories')
router.register(r'trending_books', GetTrendingBillBoardViewSet)
router.register(r'reading', UserReadingListViewSet)
router.register(r'user/library', UserLibraryAPI, basename='user-library')

urlpatterns = [
    path('search', SearchAPI),
    path('like/', LikeAPI),
    path('like/<int:pk>/', LikeAPI),
    path('read/<int:pk>/', ReadBookAPI),
    path('book/<int:pk>/', BuyBookAPI),
    # path('', CategoryViewSet.as_view(), name='books'),
    path('reading', UserReadingListViewSet.as_view({'get': 'list'})),
    # path('user/library', UserLibraryAPI.as_view({' get': 'list'})),
    # path('trending_books', GetTrendingBillBoardViewSet.as_view()),
    path('content/<int:book_id>/', getBookContentAPI),
    path('content', getBookContentAPI),
    path('upload-pdf', UploadPdfBookAPI),
    path('index', generateHomeAPI),
    path('read_html', getBookNow),
    path('user-book', UserBookAPI),
    path('publish', PublishBookAPI),
    path('genre', GetBookGenreAPI),
    path('update-book-type', UpdateBookTypeAPI),
    

]

urlpatterns += router.urls
