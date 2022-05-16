from requests import Response
from books.models import BookContent, Books, Categories, Category, CategoryItem, Genre, Like, TrendingBillboard, UserLibrary, UserReadingList, Userbook
from rest_framework import serializers



class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    genre = BookGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Books
        fields = "__all__"



class BookContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookContent
        fields = "__all__"


class AddToBookContentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class TrendingBillBoardSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = TrendingBillboard
        fields = ('id', 'cover', 'book')


class CategoryItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = CategoryItem
        fields = ("id", "book")


class CategorySerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ('id', 'title', 'books')


class UserReadingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = UserReadingList
        fields = "__all__"


class UserLibrarySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = UserLibrary
        fields = "__all__"


class LikeBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"


class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Userbook
        fields = "__all__"


class StartNewBookSerializer(serializers.Serializer):
    title = serializers.CharField()
    book_cover = serializers.ImageField()
    book_summary = serializers.CharField()
   
class PublishBookSerializer(serializers.Serializer):
    user_book_id = serializers.IntegerField()
    book_price = serializers.DecimalField(max_digits=10, decimal_places=2)



class UpdateBookTypeSerializer(serializers.Serializer):
    user_book_id = serializers.IntegerField()
    book_type = serializers.CharField()


class UPloadPdfBookSerializer(serializers.Serializer):
    user_book_id = serializers.IntegerField()
    book_pdf = serializers.FileField()
    
    