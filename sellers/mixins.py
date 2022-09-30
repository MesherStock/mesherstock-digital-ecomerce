from urllib import request
from .models import Seller
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order, OrderProduct
from products.models import Product
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail


class SellerAccountMixin(LoginRequiredMixin, object):
    account = None
    product = []
    transactions = []

    def get_account(self):
        user = self.request.user
        accounts = Seller.objects.filter(user=user)
        if accounts.exists() and accounts.count() == 1:
            self.account = accounts.first()
            return accounts.first()
        return None

    def get_product(self):
        account = self.get_account()
        products = Product.objects.filter(seller=account)
        self.product = products
        return products
    
    def get_transactions(self):
        products = self.get_product()
        transactions = OrderProduct.objects.filter(product__in=products)
        return transactions