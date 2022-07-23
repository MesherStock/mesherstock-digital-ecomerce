from unicodedata import name
from django.urls import path
from . import views


app_name = "order"
urlpatterns = [
    path("checkout/", views.order_checkout_view, name="chechout"),
    path("orders/", views.my_order_view, name="orders"),
    path("success/", views.my_order_view, name="success"),
    path("order/<int:order_id>/download", views.download_order, name="download"),
    path('remove/<int:product_id>/<int:order_id>/', views.remove_order_item, name="remove_item"),
    path('payment/', views.payment, name='payment'),
    # path('process-payment/', views.payment_process, name='process-payment'),
    # path('payment-done/', views.payment_done, name='payment_done'),
    # path('payment-cancelled/', views.payment_cancel, name='payment_cancelled'),
]