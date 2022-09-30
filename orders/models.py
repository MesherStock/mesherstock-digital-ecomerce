from django.db import models
from accounts.models import Account
from products.models import Product
from django.db.models.signals import pre_save, post_save
from decimal import Decimal
from django.urls import reverse



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name



    # def get_download_url(self):
    #         view_name = "order:download"
    #         return reverse(view_name, kwargs={"order_id": self.pk})

    # @property
    # def is_downloadable(self):
    #     if not self.product:
    #         return False
    #     if self.product.is_digital:
    #         return True
    #     return False



    def mark_paid(self, custom_amount=None, save=False):
        paid_amount = self.total
        if custom_amount != None:
            paid_amount = custom_amount
        self.paid = paid_amount
        self.status = "Completed"
        # if not self.inventory_updated and self.product:
        #     self.product.remove_item(save=True, count=1)
        #     self.inventory_updated = True
        if save == True:
            self.save()
        return self.paid


#     def calculate(self,save=False):
#         if not self.product:
#             return {}
#         subtotal = self.product.price
#         tax_rate = Decimal(0.12)
#         tax_total = (subtotal * tax_rate)
#         tax_total = Decimal("%.2f" %(tax_total))
#         total = subtotal + tax_total
#         total = Decimal("%.2f" %(total))

#         totals = {
#             "subtotal": subtotal,
#             "tax": tax_total,
#             "total": total
#         }
#         for k,v in totals.items():
#             setattr(self, k, v)
#             if save == True:
#                 self.save()
#         return self.total

# def order_pre_save(sender, instance, *args, **kwargs):
#     instance.calculate(save=False)
# pre_save.connect(order_pre_save, sender=Order)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title        

    def get_download_url(self):
            view_name = "order:download"
            return reverse(view_name, kwargs={"order_id": self.pk})


    @property
    def is_downloadable(self):
        if not self.product:
            return False
        if self.product.is_digital:
            return True
        return False

