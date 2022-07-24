from pathlib import Path
import logging
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import json
from django.urls import reverse
import pathlib
from urllib import response
from wsgiref.util import FileWrapper
from mimetypes import guess_type
import mimetypes
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Order, Payment
from .forms import OrderForm
from products.models import Product
from django.conf import settings
from decimal import Decimal
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


@login_required
def payment(request):
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    order = Order.objects.get(user=request.user, status='paid', id=body['orderID'])
    print(order)

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.status = 'paid'
    order.save()

    data = {
        'id': order.id,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)





@login_required
def my_order_view(request):
    qs = Order.objects.filter(user=request.user, status="paid")
    context = {
        "object_list": qs,
    }
    return render(request, "orders/my_order.html", context)



@login_required
def order_checkout_view(request):
    product_id = request.session.get("product_id")
    if product_id == None:
        return redirect("/")
    product = None
    try:
        product = Product.objects.get(id=product_id)
    except:
        # messages.success()
        return redirect("/")

    # if not product.has_inventory():
    #     return redirect("/no-inventory")
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
            order_obj = Order.objects.create(product=product, user=user)
    request.session['order_id'] = order_obj.id
    order_obj.mark_paid(save=True)
    # ??
    # form = OrderForm(request.POST or None, product=product, instance=order_obj)
    # if form.is_valid():
    #     order_obj.shipping_address = form.cleaned_data.get("shipping_address")
    #     order_obj.billing_address = form.cleaned_data.get("billing_address")
    #     # order_obj.mark_paid(save=False)
    #     order_obj.save()
    #     # del request.session['order_id']
    #     request.session['checkout_success_order_id'] = order_obj.id
    #     # return redirect("order:payment")
    #     return render()


    context = {
        'object':order_obj,
        # "form": form,
        "is_digital": product.is_digital,
    }
    return render(request, "orders/payment.html", context)


@login_required
def download_order(request,order_id=None, *args, **kwargs):
    if order_id == None:
        return redirect("orders/")
    qs = Order.objects.filter(id=order_id, user=request.user,product__media__isnull=False, status="paid")
    if not qs.exists():
        return redirect("orders/")
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
    if not path.exists():
        print("Nothing Came out")
        raise Http404
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