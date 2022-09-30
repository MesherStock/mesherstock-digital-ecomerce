from django.contrib import admin
from .models import Order, OrderProduct, Payment
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('payment', 'user', 'product','quantity', 'product_price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', "status"]
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)

admin.site.register(Payment)
admin.site.register(OrderProduct)


