from django.urls import path
from payment import api


urlpatterns = [
    path('flutterwave/card', api.cardPaymentAPI),
    path('flutterwave/verify', api.verifyPaymentAPI),

]
