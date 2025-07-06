from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Product
import json
from .serializers import CartItemSerializer,CartWithItemsSerializer   # import this


# Create your views here.
def recalculate_cart(cart):
    items = cart.items.all()
    total_price = sum(item.price * item.quantity for item in items)
    total_discounted_price = sum(item.discounted_price * item.quantity for item in items)
    total_item = sum(item.quantity for item in items)

    cart.total_price = total_price
    cart.total_discounted_price = total_discounted_price
    cart.total_item = total_item
    cart.save()



class AddToCartAPIView(APIView):
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        product_id = serializer.validated_data['product_id']
        quantity_delta = serializer.validated_data['quantity']  # could be +1 or -1
        product = Product.objects.get(id=product_id)

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)

            new_quantity = cart_item.quantity + quantity_delta

            if new_quantity <= 0:
                cart_item.delete()
                recalculate_cart(cart)
                return Response({"msg": "Item removed from cart","data":None}, status=status.HTTP_200_OK)
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
        except CartItem.DoesNotExist:
            if quantity_delta <= 0:
                return Response({"msg": "Cannot reduce quantity. Item not in cart."}, status=status.HTTP_400_BAD_REQUEST)

            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                user_id=user_id,
                price=product.price,
                discounted_price=product.discounted_price,
                quantity=quantity_delta,
                size='default'
            )

        recalculate_cart(cart)
        response_data = CartItemSerializer(cart_item).data
        return Response({"msg": "Cart Updated Successfully", "data": response_data}, status=status.HTTP_200_OK)
    


class CartDetailAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response({
                "cart_id": None,
                "total_price": 0,
                "total_discounted_price": 0,
                "total_item": 0,
                "items": []
            }, status=status.HTTP_200_OK)

        serializer = CartWithItemsSerializer(cart)
        data = serializer.data
        data["cart_id"] = data.pop("id")  # Rename for clarity
        return Response(data, status=status.HTTP_200_OK)
    

class ClearCartAPIView(APIView):
    def delete(self, request):
        user_id = request.user.id

        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response({"msg": "Cart already empty."}, status=status.HTTP_200_OK)

        # Delete all cart items
        CartItem.objects.filter(cart=cart).delete()

        # Reset cart totals
        cart.total_price = 0
        cart.total_discounted_price = 0
        cart.total_item = 0
        cart.save()

        return Response({"msg": "Cart cleared successfully."}, status=status.HTTP_200_OK)


