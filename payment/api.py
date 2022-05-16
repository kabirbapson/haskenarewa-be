from django.http import JsonResponse
from payment.models import BookOrder
from payment.gen_form import generate_flutter_card_form
from books.models import Books, UserLibrary
from payment import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
import string
import random

from django.conf import settings
from core.settings import flw


def gen_random_string():
    """
    Generate random unique reference character

    """
    characters = string.ascii_letters + string.digits

    while(True):
        tx_ref = ''.join(random.choices(characters, k=10))
        if BookOrder.objects.filter(tx_ref=tx_ref).count() == 0:
            break
    return tx_ref


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def cardPaymentAPI(request):
    DEFAULT_CURRENCY = "NGN"

    #
    #   Check if the form is valid
    serializer = serializers.CardPaymentSerializer(data=request.data)
    #   if not raise an exception
    serializer.is_valid(raise_exception=True)
    #
    books = serializer.data.get('books', None)
    user = request.user

    # get the list of books in database
    book_list = Books.objects.filter(pk__in=books)

    # calculate their price
    amount = [book.price for book in book_list]
    amount = sum(amount)

    tx_ref = gen_random_string()

    customer = {
        'email': user.email,
        "phonenumber": user.phone_number,
        "name": f"{user.first_name} {user.last_name}"
    }

    url = f'{settings.BASE_URL}/payment/flutterwave/verify'

    payload = generate_flutter_card_form(
        tx_ref=tx_ref, amount=amount, currency=DEFAULT_CURRENCY, redirect_url=url, customer=customer)

    response = flw.standard(payload)

    if response != 500 and response.status_code < 300:
        payment_init = response.json()
        res_status = status.HTTP_200_OK
        # save user order for completion
        book_order = BookOrder(
            user=user, pay_using='card', service='flutterwave', tx_ref=tx_ref, amount=amount)
        book_order.save()

        for book in book_list:
            book_order.books.add(book)

    else:
        print('server error trying to make payment using flutter')
        payment_init = {'status': 'failed'}
        res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(payment_init, status=res_status)


@api_view(['GET'])
def verifyPaymentAPI(request):

    if(request.GET.get('status') == 'successful'):
        orderItem = BookOrder.objects.get(tx_ref=request.GET.get('tx_ref'))
        response = flw.verify(txRef=request.GET.get('transaction_id'))
        if response != 500 and response.status_code < 300:
            response = response.json()
        else:
            return Response(status=status.HTTP_200_OK)

        if (
                response['data']['status'] == 'successful'
                and response['data']['amount'] == orderItem.amount
                and response['data']['currency'] == "NGN"
                and orderItem.status != 'completed'
        ):
            user = orderItem.user
            for book in orderItem.books.all():
                UserLibrary.objects.create(user=user, book=book)
            orderItem.status = 'completed'
            orderItem.save()
        else:
            # something fishy happen
            return Response(status=status.HTTP_200_OK)

    else:
        # user cancel the transfer
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_200_OK)
