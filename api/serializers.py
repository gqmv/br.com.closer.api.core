from rest_framework import serializers


class PurchaseSerializer(serializers.Serializer):
    """
    Serializer responsible for parsing the purchase registration request.
    """

    user_tax_id = serializers.CharField()
    store_id = serializers.IntegerField()
    item_id = (
        serializers.CharField()
    )  # Different systems might use different id formats. To account for that, we use a string.
    item_qty = serializers.IntegerField()
