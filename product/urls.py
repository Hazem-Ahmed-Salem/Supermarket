from django.urls import path
from . import views
urlpatterns = [
    path('add_products/', views.add_products, name='add_products'),
    path('preview/', views.product_preview, name='product_preview'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('decrease_stock',views.decrease_stock,name='decrease_stock')
]