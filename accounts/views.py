import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum, F, Count

from .forms import SignUpForm
from .models import User
from catalog.models import Product, Category, Order
from catalog.forms import ProductCreateForm


# -----------------------------------------
# Customer Authentication & Dashboard
# -----------------------------------------

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('accounts:customer_dashboard')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to Wellful Home!')
            return redirect('accounts:customer_dashboard')
    else:
        form = SignUpForm()
        
    return render(request, 'accounts/signup.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('accounts:customer_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'accounts:customer_dashboard'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='accounts:login')
def customer_dashboard(request):
    viewed_ids = request.session.get('viewed_product_ids', [])
    viewed_products = []
    if viewed_ids:
        products_dict = {
            p.id: p for p in Product.objects.filter(id__in=viewed_ids, is_active=True).select_related('category')
        }
        viewed_products = [products_dict[pid] for pid in viewed_ids if pid in products_dict]

    orders = (
        request.user.orders
        .prefetch_related('items__product__category')
        .order_by('-created_at')
    )

    total_orders_count = orders.count()
    completed_orders_count = orders.filter(status=Order.Status.DELIVERED).count()
    total_spent_ghs = orders.filter(
        status__in=[Order.Status.PROCESSING, Order.Status.DISPATCHED, Order.Status.DELIVERED]
    ).aggregate(total=Sum('total_amount_ghs'))['total'] or 0

    context = {
        'orders': orders,
        'viewed_products': viewed_products,
        'total_orders_count': total_orders_count,
        'completed_orders_count': completed_orders_count,
        'total_spent_ghs': total_spent_ghs,
    }
    return render(request, 'accounts/dashboard.html', context)


# -----------------------------------------
# Internal Staff & Supreme Admin Portal
# -----------------------------------------

def admin_sign_in(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('accounts:admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('accounts:admin_dashboard')
            else:
                messages.error(request, 'Access denied. Authorized personnel only.')
                return redirect('accounts:admin_login')
        else:
            messages.error(request, 'Invalid administrative credentials.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/admin_login.html', {'form': form})


def admin_sign_out(request):
    logout(request)
    messages.info(request, 'Administrative session terminated.')
    return redirect('accounts:admin_login')


@login_required(login_url='accounts:admin_login')
def admin_dashboard(request):
    """
    Tiered Portal Dispatcher:
    - Superuser: Executive analytics, financial revenue, staff access control.
    - Employee Admin: Daily logistics, inventory restock, GPS dispatch, product intake.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Staff clearance required.')
        return redirect('home')

    # Operational data shared across staff operations
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=5, stock_quantity__gt=0)
    out_of_stock_products = Product.objects.filter(stock_quantity=0)
    categories = Category.objects.prefetch_related('products').all().order_by('name')

    # Shared order pipeline
    recent_orders = Order.objects.prefetch_related('items__product', 'user').order_by('-created_at')[:10]
    inventory_products = Product.objects.select_related('category').order_by('stock_quantity')[:15]

    # 1. SUPREME SUPER ADMIN DISPATCH
    if request.user.is_superuser:
        inventory_valuation = Product.objects.aggregate(
            total_val=Sum(F('price_ghs') * F('stock_quantity'))
        )['total_val'] or 0

        total_revenue = Order.objects.filter(
            status__in=[Order.Status.PROCESSING, Order.Status.DISPATCHED, Order.Status.DELIVERED]
        ).aggregate(total=Sum('total_amount_ghs'))['total'] or 0

        pillar_data = (
            Category.objects.annotate(
                product_count=Count('products'),
                pillar_valuation=Sum(F('products__price_ghs') * F('products__stock_quantity'))
            ).values('name', 'product_count', 'pillar_valuation')
        )

        pillar_labels = [p['name'] for p in pillar_data]
        pillar_valuations = [float(p['pillar_valuation'] or 0) for p in pillar_data]
        pillar_counts = [p['product_count'] for p in pillar_data]

        context = {
            'is_super_admin': True,
            'total_products': total_products,
            'active_products': active_products,
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'categories': categories,
            'recent_orders': recent_orders,
            'inventory_products': inventory_products,
            'order_statuses': Order.Status.choices,
            'total_users': User.objects.count(),
            'total_staff': User.objects.filter(is_staff=True).count(),
            'inventory_valuation': inventory_valuation,
            'total_revenue': total_revenue,
            'staff_members': User.objects.filter(is_staff=True).order_by('-date_joined'),
            'all_users': User.objects.order_by('-date_joined')[:6],
            'chart_pillar_labels': json.dumps(pillar_labels),
            'chart_pillar_valuations': json.dumps(pillar_valuations),
            'chart_pillar_counts': json.dumps(pillar_counts),
        }
        return render(request, 'accounts/admin_dashboard.html', context)

    # 2. EMPLOYEE ADMIN (STAFF) DISPATCH
    pending_dispatch_orders = Order.objects.filter(status__in=[Order.Status.PROCESSING, Order.Status.DISPATCHED])
    product_form = ProductCreateForm()

    context = {
        'is_super_admin': False,
        'total_products': total_products,
        'active_products': active_products,
        'low_stock_count': low_stock_products.count(),
        'out_of_stock_count': out_of_stock_products.count(),
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'recent_orders': recent_orders,
        'pending_dispatch_orders': pending_dispatch_orders,
        'inventory_products': inventory_products,
        'order_statuses': Order.Status.choices,
        'product_form': product_form,
        'categories': categories,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


# -----------------------------------------
# Action Handlers
# -----------------------------------------

@login_required(login_url='accounts:admin_login')
@require_POST
def admin_update_order_status(request, order_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Unauthorized action.')
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in Order.Status.values:
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.order_number} status updated to {order.get_status_display()}.")
    else:
        messages.error(request, "Invalid order status value.")
    return redirect('accounts:admin_dashboard')


@login_required(login_url='accounts:admin_login')
@require_POST
def admin_update_stock(request, product_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Unauthorized action.')
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    try:
        qty = int(request.POST.get('stock_quantity', 0))
        if qty >= 0:
            product.stock_quantity = qty
            product.save()
            messages.success(request, f"Stock updated to {qty} for {product.name}.")
        else:
            messages.error(request, "Stock quantity cannot be negative.")
    except (ValueError, TypeError):
        messages.error(request, "Invalid numerical value for stock.")
    return redirect('accounts:admin_dashboard')


@login_required(login_url='accounts:admin_login')
def admin_create_product(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Unauthorized action.')
        return redirect('home')

    if request.method == 'GET':
        return redirect('catalog:admin_product_create')

    form = ProductCreateForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save()
        messages.success(request, f"Product '{product.name}' (SKU: {product.sku}) added to catalog.")
    else:
        messages.error(request, "Could not save product. Please check all required fields and ensure the SKU is unique.")
    return redirect('accounts:admin_dashboard')


@login_required(login_url='accounts:admin_login')
@require_POST
def admin_toggle_staff(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Only the Supreme Admin can alter employee roles.")
        return redirect('accounts:admin_dashboard')

    target_user = get_object_or_404(User, id=user_id)
    if target_user.is_superuser:
        messages.error(request, "Supreme Admin permissions cannot be modified.")
        return redirect('accounts:admin_dashboard')

    target_user.is_staff = not target_user.is_staff
    target_user.role = User.Role.ADMIN if target_user.is_staff else User.Role.SENIOR
    target_user.save()

    status_label = "promoted to Employee Admin" if target_user.is_staff else "revoked to Standard User"
    messages.success(request, f"User {target_user.username} {status_label}.")
    return redirect('accounts:admin_dashboard')