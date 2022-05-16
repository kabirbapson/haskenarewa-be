from django.urls import path
from .api import generateHome

urlpatterns = [
    path('', generateHome)
]
