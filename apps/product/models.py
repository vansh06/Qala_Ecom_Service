from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from decimal import Decimal



class Category(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

def upload_to(instance, filename):
    # Save to 'products/<product_id_or_title>/<filename>'
    return os.path.join('products', instance.title.replace(' ', '_'), filename)

class Product(models.Model):
    sq_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=100, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.FloatField(default=0.0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    image_url = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_url1 = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_url2 = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_url3 = models.ImageField(upload_to=upload_to, null=True, blank=True)

    quantity = models.IntegerField(default=0)
    stock_status = models.CharField(max_length=100, choices=[('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], default='in_stock')
    num_ratings = models.FloatField(default=0.0)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # Auto-calculate discounted price based on discount_percent
        if self.discount_percent is not None:
            # Convert float to Decimal to avoid mixing types
            multiplier = Decimal('1') - (Decimal(str(self.discount_percent)) / Decimal('100'))
            # Calculate and round to 2 decimal places
            self.discounted_price = (self.price * multiplier).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'Product'


    def __str__(self):
        return self.title
    


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.BigIntegerField(null=True, blank=True)  # Store the user_id instead of the whole User object
    review = models.TextField()
    rating     = models.PositiveSmallIntegerField(
                   choices=[(i,i) for i in range(1,6)],
                   default=5,
                   help_text="1 (worst) to 5 (best)"
                )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
        unique_together = ('product', 'user_id')  # 1 user, 1 review per product
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by user_id {self.user_id} on {self.product.title}"
    



@receiver([post_save, post_delete], sender=Review)
def update_product_average(sender, instance, **kwargs):
    product = instance.product
    # Compute the average of all related Review.rating values
    avg = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0
    # Round to two decimals and store in num_ratings
    product.num_ratings = round(avg, 2)
    product.save()


