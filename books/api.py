
from multiprocessing import context
import re
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.mixins import ListModelMixin

from books.serializers import AddToBookContentSerializer, BookGenreSerializer, BookSerializer, CategoryItemSerializer, CategorySerializer, LikeBookSerializer, PublishBookSerializer, StartNewBookSerializer, TrendingBillBoardSerializer, BookContentSerializer, UPloadPdfBookSerializer, UpdateBookTypeSerializer, UserBookSerializer,  UserLibrarySerializer, UserReadingListSerializer
from .models import BookContent, Books, Categories, Category, Genre, Like, TrendingBillboard, UserLibrary, UserReadingList, Userbook

import random


class GetBooksViewSet(viewsets.ModelViewSet):

    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class GetTrendingBillBoardViewSet(viewsets.ModelViewSet):

    queryset = TrendingBillboard.objects.all()
    serializer_class = TrendingBillBoardSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class BookAPI(viewsets.ModelViewSet):

    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class UserReadingListViewSet(viewsets.ModelViewSet):

    queryset = UserReadingList.objects.all()
    serializer_class = UserReadingListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = UserReadingList.objects.all().filter(
            user=self.request.user).order_by('-date_read')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # if self.request.user.id != request.data['user']:
        #     return Response({'failed': 'user is not a valid'}, status=status.HTTP_400_BAD_REQUEST)
        # reading = self.queryset.filter(user=request.user)
        # same_book = reading.filter(book=request.data['book'])

        # if len(reading) != 0 and len(same_book) != 0:
        #     return Response(status=status.HTTP_200_OK)
        # book = serializer.save()
        # reading_list = UserReadingListSerializer(
        #     book, context=self.get_serializer()).data,

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
# @authentication_classes([IsAuthenticated])
def SearchAPI(request):

    query = request.GET.get('q', None)
    if query == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    result = Books.objects.filter(title__icontains=query)
    transformer = BookSerializer(
        result, context={'request': request}, many=True)
    return Response(transformer.data, status=200)


@api_view(['GET', 'POST', 'PUT'])
def getBookContentAPI(request, book_id=None):

    if request.method == 'GET':
        if book_id == None:
            return Response(status=404)

        try:

            book = Books.objects.get(id=book_id)

        except Exception as Err:
            return Response(status=404)
        content = BookContent.objects.all().filter(book=book)

        serializer = BookContentSerializer(
            content,  many=True)
        return Response(serializer.data, status=200)

    if request.method == 'POST':
        serializer = AddToBookContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_books = Userbook.objects.get(id=serializer.data['id'])
        book = user_books.book

        book_content = BookContent(
            book=book, chapter=serializer.data['title'])

        book_content.save()

        ser = BookContentSerializer(book_content)

        return Response(ser.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = BookContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            book_content = BookContent.objects.get(id=book_id)
        except Exception as error:
            return Response(status=status.HTTP_404_NOT_FOUND)

        book_content.content = serializer.data['content']
        book_content.save()

        serializer = BookContentSerializer(book_content)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLibraryAPI(viewsets.ReadOnlyModelViewSet):

    queryset = UserLibrary.objects.all()
    serializer_class = UserLibrarySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = UserLibrary.objects.all().filter(
            user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def generateHomeAPI(request):
    books = Books.objects.all().filter(status='publish')

    category = Category.objects.all()

    categories = [{'id': x.id, 'title': x.name} for x in category]
    for item in categories:
        item['books'] = []
        y = []

        while(len(item['books']) < 10):
            r_number = random.randrange(len(books))
            if r_number not in y:
                y.append(r_number)
                item['books'].append(BookSerializer(
                    books[r_number], context={'request': request}).data)

    return Response(categories, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def LikeAPI(request, pk=None):

    if request.method == 'GET':
        like_books = Like.objects.all().filter(user=request.user)
        return Response(LikeBookSerializer(like_books, context={'request': request}, many=True).data, status=status.HTTP_201_CREATED)

    try:
        book = Books.objects.get(id=pk)
    except Exception as error:
        return Response(status=status.HTTP_404_NOT_FOUND)
    check_if_liked = Like.objects.all().filter(book=book).filter(user=request.user)

    if len(check_if_liked) != 0:
        book.likes -= 1
        book.save()
        like = check_if_liked[0]
        like.delete()
        like_books = Like.objects.all().filter(user=request.user)
        return Response(LikeBookSerializer(like_books, context={'request': request}, many=True).data, status=status.HTTP_201_CREATED)

    book.likes += 1
    book.save()
    Like.objects.create(book=book, user=request.user)
    like_books = Like.objects.all().filter(user=request.user)
    return Response(LikeBookSerializer(like_books, context={'request': request}, many=True).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def BuyBookAPI(request, pk=None):
    try:
        book = Books.objects.get(id=pk)
    except Exception as error:
        return Response(status=status.HTTP_404_NOT_FOUND)
    check_if_own = UserLibrary.objects.all().filter(
        book=book).filter(user=request.user)
    if check_if_own:
        return Response({'you already own the book': True}, status=status.HTTP_200_OK)
    return Response({"you don't have this book": False}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ReadBookAPI(request, pk=None):
    try:
        book = Books.objects.get(id=pk)
    except Books.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        reading = UserReadingList.objects.get(
            user=request.user, book=book)
        # exist update the reading time
        reading.date_read = timezone.now()
        reading.save()
    except UserReadingList.DoesNotExist:
        # mean we don't have it on our reading list
        # and we can add the book to the reading list
        reading = UserReadingList(user=request.user, book=book)
        reading.save()

    return Response(UserReadingListSerializer(UserReadingList.objects.all().order_by('-date_read'), context={'request': request}, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def UserBookAPI(request):

    if request.method == 'GET':
        user_book = Userbook.objects.filter(
            owner=request.user).order_by('-last_time_edit')
        serializer = UserBookSerializer(
            user_book, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = StartNewBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # return Response(data=request.FILES['book_cover'], status=status.HTTP_200_OK)

        book = Books(title=serializer.data['title'], book_cover=request.FILES['book_cover'],
                     book_summary=serializer.data['book_summary'], author=request.user)

        book.save()

        user_book = Userbook(book=book, owner=request.user)
        user_book.save()

        ser = UserBookSerializer(user_book, context={'request': request})

        return Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def UserBookAPI(request):

    if request.method == 'GET':
        user_book = Userbook.objects.filter(
            owner=request.user).order_by('-last_time_edit')
        serializer = UserBookSerializer(
            user_book, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        serializer = StartNewBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # return Response(data=request.FILES['book_cover'], status=status.HTTP_200_OK)

        genre = request.data['genre']
        if genre == '':
            genre = []
        else:
            genre = genre.split(',')

        genre_list = Genre.objects.filter(pk__in=genre)

        book = Books(title=serializer.data['title'], book_cover=request.FILES['book_cover'],
                     book_summary=serializer.data['book_summary'], author=request.user)

        book.save()

        if(len(genre_list) != 0):
            book.genre.set(genre_list)

        user_book = Userbook(book=book, owner=request.user)
        user_book.save()

        ser = UserBookSerializer(user_book, context={'request': request})

        return Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PublishBookAPI(request):
    serializer = PublishBookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user_book = Userbook.objects.get(id=serializer.data['user_book_id'])
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_book.book.status = 'publish'
    user_book.book.price = serializer.data['book_price']
    user_book.book.publication_date = timezone.now()
    user_book.book.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetBookGenreAPI(request):

    genre = Genre.objects.all()

    serializer = BookGenreSerializer(genre, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateBookTypeAPI(request):

    serializer = UpdateBookTypeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        user_book = Userbook.objects.get(id=serializer.data['user_book_id'])   
    except Userbook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user_book.book.content_type = serializer.data['book_type']
    user_book.book.save()
    
    transform = UserBookSerializer(user_book, context={'request': request},)
    
    return Response(transform.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UploadPdfBookAPI(request):
    serializer = UPloadPdfBookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # return Response(data=request.FILES['book_cover'], status=status.HTTP_200_OK)

    user_book = Userbook.objects.get(id=serializer.data['user_book_id'])
    
    try:
        book_content = BookContent.objects.filter(book=user_book.book)
        book_content.pdf = request.FILE['book_pdf']
        book_content.save()
    except BookContent.DoesNotExist:
        book_content = BookContent(book=user_book.book, pdf=request.FILE['book_pdf'])
        book_content.save()
                
    transform = BookContentSerializer(book_content)  

    return Response(transform.data, status=status.HTTP_201_CREATED)

    
    
