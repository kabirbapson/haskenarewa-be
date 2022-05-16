from django.db import models
from django.conf import settings

from books.models import Books

# Create your models here.


class BookOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    books = models.ManyToManyField(Books)
    pay_using = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    tx_ref = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='pending')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
