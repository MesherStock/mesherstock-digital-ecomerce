
from django.urls import path

from orders import views
from .views import (
    SellerDashBoard,
    SellerProducts,
    TransactionListView,
    

)
from products.views import (
    ProductCreateView,
    ProductUpdateView,
)

app_name = "seller"
urlpatterns = [
    
    path("seller/product/add", ProductCreateView.as_view(), name="create"),
    # path("product/<slug:slug>/update", ProductUpdateView.as_view(), name="update"),
    
    path("seller/dashboard/", SellerDashBoard.as_view(), name="dashboard"),
    path("seller/product_all/", SellerProducts.as_view(), name="seller_products"),
    path("seller/transactions/", TransactionListView.as_view(), name="transactions"),
    path("transaction_all", TransactionListView.as_view(), name="transaction"),
    path("seller/product/<slug:slug>/update", ProductUpdateView.as_view(), name="update_product"),
   
    
]