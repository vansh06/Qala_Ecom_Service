from django.db import models




# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    role = models.SmallIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)


    class Meta:
        db_table = "users"  # Match your MySQL table name

    def __str__(self):
        return self.email if self.email else f"User {self.id}"
    
        # ✅ Required for DRF permissions like IsAuthenticated
    @property
    def is_authenticated(self):
        return True