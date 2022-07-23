from django import forms
from .models import InventoryWaitList

class InventoryWaitListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product") or None
        super().__init__(*args, **kwargs)
        self.product = product

    class Meta:
        model = InventoryWaitList
        fields = [
            "email",
        ]
    
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        email = self.cleaned_data.get('email')
        qs = InventoryWaitList.objects.filter(product=self.product, email__iexact=email)
        if qs.count() > 5:
            error_msg = "10-4 we have your waitlist entry for this product"
            raise forms.ValidationError(error_msg)

        return data
    