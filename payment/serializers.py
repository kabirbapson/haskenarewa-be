from rest_framework import serializers


class CardPaymentSerializer(serializers.Serializer):
    books = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            min_value=None, max_value=None)
    )
