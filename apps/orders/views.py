from django.shortcuts import render

# Create your views here.
# orders/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import hmac
import hashlib
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from address.models import Address
from product.models import Product
from .serializers import CreateOrderSerializer
import logging
import razorpay
from rest_framework.permissions import AllowAny


RAZORPAY_API_KEY='rzp_test_LXbbVUj49yDXf7'
RAZORPAY_API_SECRET='Y98uMFwlasuPsvFGeRCDlVd8'

logger = logging.getLogger('qalakarwaan')


class CreateOrderView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # serializer = CreateOrderSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        user = request.user

        id = user.id

        shipping_address_id = request.data.get('shipping_address_id')

        # Get address
        try:
            shipping_address = Address.objects.get(id=shipping_address_id, user_id=id)
        except Address.DoesNotExist:
            return Response({"error": "Invalid shipping address."}, status=400)
        except Exception as e:
            return Response({"error":"Unknown error which fetching the address","details":str(e)}, status=500)

        # Get cart items
        try:
            cart = Cart.objects.get(user_id=user.id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=400)
        except Exception as e:
            return Response({"error":"Unknown error which fetching the cart items","details":str(e)}, status=500)

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=400)

        # Totals & data
        total_price = 0
        total_discounted_price = 0
        total_items = 0
        sq_id_list = []
        order_items_data = []

        for item in cart_items:
            product = item.product
            quantity = item.quantity
            if not product:
                continue

            total_price += product.price * quantity
            total_discounted_price += product.discounted_price * quantity
            total_items += quantity
            sq_id_list.append(product.sq_id)

            order_items_data.append({
                "product": product,
                "user": user,
                "price": product.price,
                "discounted_price": product.discounted_price,
                "quantity": quantity
            })


        try:
            # Create Razorpay order
            client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
            razorpay_order = client.order.create({
                "amount": int(total_discounted_price * 100),
                "currency": "INR",
                "payment_capture": 1
            })



            # Create Order
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                order_status='ORDER_PLACED',
                status='PENDING',
                total_price=total_price,
                total_discounted_price=total_discounted_price,
                total_items=total_items,
                sq_id_list=sq_id_list,
                razorpay_order_id=razorpay_order['id']
            )

            # Create OrderItems
            for item in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    user=item['user'],
                    price=item['price'],
                    discounted_price=item['discounted_price'],
                    quantity=item['quantity']
                )

            # Clear cart
            cart_items.delete()

            cart.total_price = 0
            cart.total_discounted_price = 0
            cart.total_item = 0
            cart.save()

            return Response({
                "message": "Order created successfully.",
                "order_id": order.id,
                "razorpay_order_id": order.razorpay_order_id,
                "amount": order.total_discounted_price,
                "currency": "INR"
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error":"Error in placing Order, Try Again after Some Time","details":str(e)}, status=500)




class RazorpayVerifyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Prevents JWT errors
    def post(self, request):
        data = request.data
        print("FULL RESPONSE FROM RAZORPAY-->",data)
        order_id = data.get("razorpay_order_id")
        payment_id = data.get("razorpay_payment_id")
        signature = data.get("razorpay_signature")

        logger.warning(f" Verfication Details--->{order_id},{payment_id},{signature}")
        print(f" Verfication Details--->{order_id},{payment_id},{signature}")


         # Validate signature
        try:
            generated_signature = hmac.new(
                key=RAZORPAY_API_SECRET.encode(),
                msg=f"{order_id}|{payment_id}".encode(),
                digestmod=hashlib.sha256
            ).hexdigest()

            if generated_signature != signature:
                return Response({"success": False, "error": "Invalid signature"}, status=400)

            # ✅ Update order in DB
            try:
                order = Order.objects.get(razorpay_order_id=order_id)
                order.razorpay_payment_id = payment_id
                order.razorpay_signature = signature
                order.status = "PAID"
                order.order_status = "ORDER_PLACED"  # Optional: adjust based on your logic
                order.save()

                logger.info(f"✅ Payment verified for Order ID: {order.id}")
                return Response({"success": True, "message": "Payment verified and order updated."})

            except Order.DoesNotExist:
                logger.error(f"❌ Order not found for Razorpay Order ID: {order_id}")
                return Response({"success": False, "error": "Order not found."}, status=404)

        except Exception as e:
            logger.exception("❌ Unexpected error during Razorpay verification")
            return Response({"success": False, "error": "Server error", "details": str(e)}, status=500)




