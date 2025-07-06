from django.contrib import admin

# Register your models here.

from .models import Cart, CartItem
from .views import recalculate_cart

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    can_delete = False  # ✅ disables the "delete" checkbox
    readonly_fields = ['product', 'price', 'discounted_price', 'size', 'user_id','quantity']
    fields = ['product', 'price', 'discounted_price', 'size', 'user_id', 'quantity']

    # def save_formset(self, request, form, formset, change):
    #     super().save_formset(request, form, formset, change)
    #     # Recalculate cart totals after inline save
    #     recalculate_cart(form.instance)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'total_item', 'total_price', 'total_discounted_price']
    readonly_fields = ['id', 'user_id', 'total_item', 'total_price', 'total_discounted_price']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'user_id', 'quantity', 'price', 'discounted_price', 'size']
    list_filter = ['cart', 'product']
    search_fields = ['product__title', 'cart__user_id']
    readonly_fields = ['product', 'price', 'discounted_price', 'size', 'user_id']
    fields = ['cart', 'product', 'user_id', 'quantity', 'price', 'discounted_price', 'size']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        recalculate_cart(obj.cart)
