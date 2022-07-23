from itertools import product
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(label="", required=False ,widget=(
        forms.Textarea(attrs={
            "class": "shipping-address-class form-control",
            "placeholder":"Your Shipping address",
            "rows": 3
        })
    ))
    billing_address = forms.CharField(label="", widget=(
        forms.Textarea(attrs={
            "class": "billing-address-class form-control",
            "placeholder":"Your billing address",
            "rows": 3
        })
    ))

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product") or None
        super().__init__(*args, **kwargs)
        self.product = product

    class Meta:
        model = Order
        fields = [
            "shipping_address",
            "billing_address",
        ]
    
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        shipping_addr = self.cleaned_data.get("shipping_address")
        billing_addr = self.cleaned_data.get("billing_address")
        if self.product != None:
            if not self.product.can_order:
                raise forms.ValidationError("This product can not be ordered at this time")
            if (self.product.requires_shipping and shipping_addr=="") or (self.product.requires_shipping and shipping_addr==None):
                print(self.product.requires_shipping and shipping_addr)
                self.add_error("shipping-addr", "This product requires a shipping address.")
                # raise forms.ValidationError("Please enter your shipping address")
        return data
    