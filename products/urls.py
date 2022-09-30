from unicodedata import name
from django.urls import path
from . import views
from .views import (
    VendorListView
)


from django.views.generic.base import RedirectView

app_name = "product"
urlpatterns = [
    path('product/feature', views.featured_view, name="featured"),
    path("", views.home_view, name="index"),
    path('product/<slug:slug>/category/', views.category_list, name='category_list'),
    path('product/category/', views.category_view, name='category_view'),
    path('product/list/', views.list_view, name="list"),
    path('product/<slug:slug>/', views.product_detail_view, name='detail'),
    path('search/', views.search_view, name="search"),
    path("vendor/<vendor_name>/", VendorListView.as_view(), name="vendor_detail"),
    path("vendor/",RedirectView.as_view(pattern_name="product:list"), name="vendor_list"),
    # path('orders/<int:order_id>/download/', views.download_order, name='download'),
]