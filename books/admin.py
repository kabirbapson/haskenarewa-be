from django.contrib import admin
from .models import BookContent, Books, Categories, Category, CategoryItem, Genre, TrendingBillboard, UserLibrary, UserReadingList, Userbook
# Register your models here.
admin.site.register(Books)
admin.site.register(TrendingBillboard)
admin.site.register(CategoryItem)
admin.site.register(Categories)
admin.site.register(Category)
admin.site.register(UserReadingList)
admin.site.register(BookContent)
admin.site.register(UserLibrary)
admin.site.register(Genre)
admin.site.register(Userbook)
