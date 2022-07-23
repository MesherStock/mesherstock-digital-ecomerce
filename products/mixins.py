from django.http import Http404
from Ecodig.mixins import LoginRequireMixin
from sellers.mixins import SellerAccountMixin


class ProductManagerMixin(SellerAccountMixin,object):
    def get_object(self, **kwargs):
        seller = self.get_account()
        obj = super(ProductManagerMixin, self).get_object(**kwargs)
        try:
            obj.user == seller
        except:
            raise Http404
        if obj.seller == seller:
            return obj
        else:
            raise Http404