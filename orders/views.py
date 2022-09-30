from pathlib import Path
import logging
import pathlib
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import json
from django.urls import reverse

from urllib import request, response
from wsgiref.util import FileWrapper
from mimetypes import guess_type
import mimetypes
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Order, OrderProduct, Payment
from .forms import OrderForm
from products.models import Product
from django.conf import settings
from decimal import Decimal
from django.views.generic import FormView
from django.urls import reverse
from carts.models import Cart, CartItem
from django.views.decorators.csrf import csrf_exempt
import urllib.request

# Order Email
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail




@login_required
def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.total,
        status = body['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product.id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # cart_item = CartItem.objects.filter(id=item.id)
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    CartItem.objects.filter(user=request.user).delete()
    current_site = get_current_site(request)
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    msg = EmailMessage(mail_subject, message, to=[to_email])
    msg.send()
    

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id
    }
    return JsonResponse(data)



@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('product:category_view')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax_rate = Decimal(0.12)
    tax = (total * tax_rate)
    tax = Decimal("%.2f" %(tax))
    grand_total = total + tax


    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            print(order.order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('cart:checkout')
        



@login_required
def my_order_view(request):
    qs = OrderProduct.objects.filter(user=request.user, ordered=True)
    context = {
        "object_list": qs,
    }
    return render(request, "orders/my_order.html", context)


@login_required
def simple_checkout(request):
    product_id = request.session.get("product_id")
    if product_id == None:
        return redirect("/")
    product = None
    try:
        product = Product.objects.get(id=product_id)
    except:
        return redirect("/")

    user = request.user # AnonUser
    order_id = request.session.get("order_id") # cart
    order_obj = None
    new_creation = False
    try:
        order_obj = Order.objects.get(id=order_id)
    except:
        order_id = None
    if order_id == None:
        new_creation = True
        order_obj = Order.objects.create(product=product, user=user)
    if order_obj != None and new_creation == False:
        if order_obj.product.id != product.id:
            order_obj = Order.objects.create(product=product, user=user, status='New')
    request.session['order_id'] = order_obj.id
    # order_obj.mark_paid(save=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_obj.billing_address = form.cleaned_data.get("billing_address")
            order_obj.first_name = form.cleaned_data.get("first_name")
            order_obj.last_name = form.cleaned_data.get("last_name")
            order_obj.tel_phone = form.cleaned_data.get('tel_phone')
            order_obj.email = form.cleaned_data.get("email")
            order_obj.country = form.cleaned_data.get("country")
            order_obj.state = form.cleaned_data.get("state")
            order_obj.city = form.cleaned_data.get("city")

            # order_obj.mark_paid(save=False)
            order_obj.save()
            # del request.session['order_id']
            # request.session['checkout_success_order_id'] = order_obj.id


    context = {
        'object':order_obj,
    }
    return render(request,"orders/payment.html", context)


@login_required
def order_checkout_view(request):
    pass








# @login_required
# def order_checkout_view(request):
#     product_id = request.session.get("product_id")
#     if product_id == None:
#         return redirect("/")
#     product = None
#     try:
#         product = Product.objects.get(id=product_id)
#     except:
#         return redirect("/")
#     user = request.user # AnonUser
#     order_id = request.session.get("order_id") # cart
#     order_obj = None
#     new_creation = False
#     try:
#         order_obj = Order.objects.get(id=order_id)
#     except:
#         order_id = None
#     if order_id == None:
#         new_creation = True
#         order_obj = Order.objects.create(product=product, user=user)
#     if order_obj != None and new_creation == False:
#         if order_obj.product.id != product.id:
#             order_obj = Order.objects.create(product=product, user=user)
#     request.session['order_id'] = order_obj.id
#     # order_obj.mark_paid(save=True)
#     # ??
#     # form = OrderForm(request.POST or None, product=product, instance=order_obj)
#     # if form.is_valid():
#     #     order_obj.billing_address = form.cleaned_data.get("billing_address")
#     #     order_obj.first_name = form.cleaned_data.get("first_name")
#     #     order_obj.last_name = form.cleaned_data.get("last_name")
#     #     order_obj.tel_phone = form.cleaned_data.get('tel_phone')
#     #     order_obj.email = form.cleaned_data.get("email")
#     #     order_obj.country = form.cleaned_data.get("country")
#     #     order_obj.state = form.cleaned_data.get("state")
#     #     order_obj.city = form.cleaned_data.get("city")
    
#     #     order_obj.save()
#     #     del request.session['order_id']
#     #     request.session['checkout_success_order_id'] = order_obj.id
        
    
#     try:
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#     except json.JSONDecodeError:
#         order_obj.mark_paid(save=True) 
#     context = {
#         'object':order_obj,
#         # "form": form,
#         "is_digital": product.is_digital,
#     }
#     return render(request, "orders/payment.html", context)


@login_required
def download_order(request,order_id=None, *args, **kwargs):
    if order_id == None:
        return redirect("orders/")
    qs = OrderProduct.objects.filter(id=order_id, user=request.user,product__media__isnull=False, ordered=True)
    # if not qs.exists():
    #     # return redirect("orders/")
    #     return Http404
    order_obj = qs.first()
    product_obj = order_obj.product
    if not product_obj.media:
        return redirect("orders/")
    media = product_obj.media
    product_path = media.path
    path = pathlib.Path(product_path)
    pk = product_obj.pk
    ext = path.suffix
    fname = f"{product_obj}-{pk}{ext}"
    with open(path, "rb") as f:
        wrapper = FileWrapper(f)
        content_type = "application/force-download"
        guess_ = guess_type(path)[0]
        if guess_:
            content_type = guess_
        response = HttpResponse(wrapper, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={fname}"
        response['X-sendFile'] = f'{fname}'
        return response



def remove_order_item(request, product_id,  order_id):
    product_id = request.session.get("product_id")
    product = get_object_or_404 (Product, id = product_id)
    order_id = request.session.get("order_id")
    if request.user.is_authenticated:
        order_item = Order.objects.get(product=product, user=request.user, id=order_id)
    else:
        order = Order.objects.get(id=order_id)
        order_item = Order.objects.get(product=product, order=order,id=order_id)
    order_item.delete()
    return redirect('/')