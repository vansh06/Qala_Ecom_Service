from django.contrib import admin
from .models import User



@admin.register(User)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id','email','first_name','last_name','mobile','active',)
    search_fields = ('email','mobile',)
    list_filter = ('active',)
    exclude = ('password',)


# Register your models here.
