from multiprocessing import managers
from django.urls import reverse
from django.db import models
from django.conf import settings
from accounts.models import Account
from products.models import User

# Create your models here.
class Seller(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    managers = models.ManyToManyField(Account, related_name="manager_sellers", blank=True)
    active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        view_name = "product:vendor_detail"
        return reverse(view_name, kwargs={"vendor_name": self.user.username})

