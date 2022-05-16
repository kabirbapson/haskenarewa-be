from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def error_404(request, exception=None):
    return render(request, '404.html', status=404)
