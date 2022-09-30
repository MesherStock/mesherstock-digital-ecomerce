from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user','product', 'quantity','is_active']
    list_editable = ['is_active',]
    list_display_links = ['product',]



admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
