from django.urls import path
from . import views


urlpatterns = [
    path('', views.about, name='about'),
    path('licencing/', views.pricing, name='licencing'),
]