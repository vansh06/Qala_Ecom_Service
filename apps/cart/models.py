from django.db import models
from product.models import Product  # assuming your product app exists

class Cart(models.Model):
    user_id = models.BigIntegerField()
    total_discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_item = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'Cart'

    def __str__(self):
        return f"Cart {self.id} - User {self.user_id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.BigIntegerField()
    Sq_id = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50)

    class Meta:
        db_table = 'CartItem'

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Cart {self.cart.id}"

