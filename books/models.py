from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.conf import settings

# Create your models here.


def save_to(instance, filename):
    # file type
    file_type = filename.split('.')[-1]

    return f"images/books/cover/{instance.title}.{file_type}"


def upload_to(instance, filename):
    # file type
    file_type = filename.split('.')[-1]
    return f"pdf/books/{instance.title}.{file_type}"


class Categories(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    books = models.ManyToManyField('Books')

    def __str__(self):
        return self.title


class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    genre = models.ManyToManyField(
        'Genre', help_text='Select a genre for this book')
    book_cover = models.ImageField(
        upload_to=save_to, default='images/books/cover/default/default.png')
    content_type = models.CharField(max_length=255, help_text='choose between write or pdf file', null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=255, default='English')
    book_summary = models.TextField(max_length=1000, null=True, blank=True)
    # publisher = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2,
                                default=0.00, help_text='write down the price of the book')
    likes = models.BigIntegerField(default=0)
    readers = models.BigIntegerField(default=0)
    ratings = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='un-publish')

    def __str__(self):
        return self.title


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class BookContent(models.Model):
    book = models.ForeignKey(Books, on_delete=models.PROTECT)
    chapter = models.CharField(max_length=255, default='')
    content = models.TextField(help_text="start writing", default='')
    pdf = models.FileField(upload_to=upload_to, null=True, default=None)


class Userbook(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    last_time_edit = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TrendingBillboard(models.Model):
    cover = models.ImageField(upload_to='images/books/trending', null=False)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.book.title


class CategoryItem(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    books = models.ForeignKey(Books, models.CASCADE)


class UserReadingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    date_read = models.DateTimeField(default=timezone.now)
    date_started_reading = models.DateTimeField(auto_now_add=True)
    progress_of_reading = models.FloatField(default=0.0)


class UserLibrary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.PROTECT)
    added_on = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100, help_text='type the category name')

    def __str__(self):
        return self.name


class Review(models.Model):
    pass


class Like(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    like_on = models.DateTimeField(auto_now_add=True)
