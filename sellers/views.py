from genericpath import exists
from django.shortcuts import redirect, render
from itertools import chain
from django.db.models import Q
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SellerAccountMixin
from .forms import NewSellerForm
from .models import Seller
from products.models import Product
from orders.models import Order, OrderProduct
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
# Create your views here.
class SellerProducts(SellerAccountMixin, ListView):
    model = Product
    template_name = "sellers/products_list_view.html"

    def get_queryset(self, **kwargs):
        qs = super(SellerProducts, self).get_queryset(**kwargs)
        qs = qs.filter(seller=self.get_account())
        query = self.request.GET.get("q", "")
        qs = qs.filter(Q(title__icontains=query)|Q(content__icontains=query))
        results = list(chain(qs))
        return results


class TransactionListView(SellerAccountMixin,ListView):
    model = Order
    template_name = "sellers/transaction_list_view.html"
    def get_queryset(self):
        return self.get_transactions


class SellerRedirectView(RedirectView):
        permanent = True
        def get_redirect_url(self, *args, **kwargs):
                obj = get_object_or_404 (Product, slug=kwargs['slug'])
                return obj.get_absolute_url()


class SellerDashBoard(SellerAccountMixin,FormMixin,View):
    form_class = NewSellerForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get(self, request, *args, **kwargs):
        apply_form = NewSellerForm()
        account = self.get_account()
        exists = account
        active = None
        context = {}
        if exists:
            active = account.active
            
        
        if not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Seller Dashboard"
            context['products'] = self.get_product()[:3]
            context['transactions'] = self.get_transactions()[:3]
        else:
            pass

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashBoard, self).form_valid(form)
        obj = Seller.objects.create(user=self.request.user)
        return valid_data