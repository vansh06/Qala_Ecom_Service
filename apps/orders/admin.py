from django.contrib import admin

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete = False  # ✅ disables the "delete" checkbox

    extra = 0
    readonly_fields = ('product', 'price', 'discounted_price', 'quantity', 'user')

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'status', 'order_status', 
        'total_discounted_price', 'total_price', 
        'total_items', 'created_at'
    )
    list_filter = ('status', 'order_status', 'created_at')
    search_fields = ('user__email', 'user__mobile', 'razorpay_order_id')
    inlines = [OrderItemInline]
    readonly_fields = (
        'user', 'shipping_address', 'status',
        'total_discounted_price', 'total_price', 'total_items',
        'sq_id_list', 'razorpay_order_id', 'razorpay_payment_id', 
        'razorpay_signature', 'created_at', 'updated_at'
    )

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order', 'product', 'user', 
        'price', 'discounted_price', 'quantity'
    )
    search_fields = ('product__title', 'order__id', 'user__email', 'user__mobile')
    readonly_fields = ('order', 'product', 'user', 'price', 'discounted_price', 'quantity')

admin.site.register(OrderItem, OrderItemAdmin)
