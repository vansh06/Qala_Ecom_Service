from rest_framework import serializers
from .models import CartItem, Product,Cart

from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    # product = serializers.SerializerMethodField(read_only=True)
    product = ProductSerializer(read_only=True)


    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'product_id', 'product', 'user_id',
            'Sq_id', 'price', 'discounted_price', 'quantity', 'size'
        ]
        read_only_fields = ['id', 'cart', 'price', 'discounted_price', 'user_id', 'Sq_id', 'size']

    # def get_product(self, obj):
    #     product = obj.product
    #     return {
    #         "id": product.id,
    #         "title": product.title,
    #         "price": product.price,
    #         "discounted_price": product.discounted_price,
    #         "discount_percent":product.discount_percent
    #     }

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product not found.")
        return value
    

class CartWithItemsSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'total_discounted_price', 'total_item', 'items']
