
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include('products.urls', namespace="products")),
    path('accounts/', include('accounts.urls', namespace="account")),
    path('', include("orders.urls", namespace='order')),
    path('', include("sellers.urls", namespace="seller")),
    path('tag/', include("tags.urls", namespace="tag")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
