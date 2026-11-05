from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Customer Authentication & Dashboard
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Internal Staff & Supreme Admin Portal
    path('portal/login/', views.admin_sign_in, name='admin_login'),
    path('portal/logout/', views.admin_sign_out, name='admin_logout'),
    path('portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Supreme & Staff Command Quick Actions
    path('portal/orders/<int:order_id>/status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('portal/products/<int:product_id>/stock/', views.admin_update_stock, name='admin_update_stock'),
    path('portal/products/create/', views.admin_create_product, name='admin_create_product'),
    path('portal/products/add/', views.admin_create_product, name='admin_product_add'),
    path('portal/users/<int:user_id>/toggle-staff/', views.admin_toggle_staff, name='admin_toggle_staff'),
]