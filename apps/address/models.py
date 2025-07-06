from django.db import models

# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)  # Storing AppUser ID directly

    class Meta:
        db_table = 'address'  # Explicitly setting table name in DB
        unique_together = ('user_id', 'mobile', 'street_address', 'zip_code')  # Define "duplicate"


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"
