# orders/serializers.py

from rest_framework import serializers

class CreateOrderSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()

    def validate_shipping_address_id(self, value):
        # Optional: Add positive int check or access control
        if value <= 0:
            raise serializers.ValidationError("Invalid address ID.")
        return value
