from django import template
from django.contrib.auth.models import Group 
from sellers.models import Seller

register = template.Library()

# @register.filter(name='has_group')
# def get_seller(user, group_name): 
#     group = Group.objects.get(name=group_name) 
#     return True if group in user.groups.all() else False



@register.filter(seller='get_seller')
def get_seller(seller, group_name): 
    group = Seller.objects.get(user=group_name) 
    return True if group in seller.user.all() else False



