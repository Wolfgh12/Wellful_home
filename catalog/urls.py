from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/quick-order/', views.quick_order_checkout, name='quick_order_checkout'),
    path('portal/product/add/', views.admin_product_create, name='admin_product_create'),
    path('portal/product/<int:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('portal/product/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),
]