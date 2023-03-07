from rest_framework import serializers


class PurchaseSerializer(serializers.Serializer):
    user_tax_id = serializers.CharField()
    store_id = serializers.IntegerField()
    item_id = serializers.CharField()
    item_qty = serializers.IntegerField()
