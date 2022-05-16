from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


@api_view(['GET'])
def generateHome(request):
    pass
