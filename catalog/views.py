from urllib.parse import quote
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Category, Product, ProductImage, Order, OrderItem
from .forms import ProductCreateForm, QuickWhatsAppOrderForm


def home(request):
    categories = Category.objects.all().order_by('name')
    categories_by_pillar = {cat.pillar_type: cat for cat in categories}
    return render(request, 'home.html', {
        'categories': categories,
        'categories_by_pillar': categories_by_pillar,
    })


def product_list(request):
    categories = Category.objects.all().order_by('name')
    products = (
        Product.objects.filter(is_active=True)
        .exclude(category__availability_status=Category.AvailabilityStatus.COMING_SOON)
        .select_related('category')
        .order_by('-created_at')
    )
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'catalog/product_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    is_staff_user = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    if category.is_locked and not is_staff_user:
        messages.info(request, f"{category.name} is currently Coming Soon. Please check back shortly or contact our wholesale desk.")
        return redirect('home')

    products = (
        category.products.filter(is_active=True)
        .select_related('category')
        .order_by('-created_at')
    )
    all_categories = Category.objects.all().order_by('name')
    
    context = {
        'category': category,
        'products': products,
        'all_categories': all_categories,
    }
    return render(request, 'catalog/category_detail.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug,
        is_active=True
    )
    is_staff_user = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    if product.category.is_locked and not is_staff_user:
        messages.info(request, f"{product.category.name} is currently Coming Soon.")
        return redirect('home')

    related_products = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(id=product.id)
        .order_by('-created_at')[:3]
    )

    # Track viewed product IDs in session (most recent first, up to 8 unique)
    viewed = request.session.get('viewed_product_ids', [])
    if product.id in viewed:
        viewed.remove(product.id)
    viewed.insert(0, product.id)
    request.session['viewed_product_ids'] = viewed[:8]
    request.session.modified = True

    order_form = QuickWhatsAppOrderForm()
    context = {
        'product': product,
        'related_products': related_products,
        'order_form': order_form,
    }
    return render(request, 'catalog/product_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@require_POST
def admin_pillar_status_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    new_status = request.POST.get('availability_status')
    valid_statuses = {choice[0] for choice in Category.AvailabilityStatus.choices}

    if new_status in valid_statuses:
        category.availability_status = new_status
        category.save(update_fields=['availability_status'])
        messages.success(
            request,
            f"Updated '{category.name}' ({category.get_pillar_type_display()}) to {category.get_availability_status_display()}."
        )
    else:
        messages.error(request, "Invalid pillar availability status selected.")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('accounts:admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_product_create(request):
    initial_data = {}
    category_id = request.GET.get('category')
    if category_id:
        initial_data['category'] = category_id

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            gallery_files = request.FILES.getlist('gallery_images')
            for img in gallery_files[:10]:
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, f"Product '{product.name}' was successfully added to {product.category.name}!")
            return redirect('accounts:admin_dashboard')
    else:
        form = ProductCreateForm(initial=initial_data)

    categories = Category.objects.all().order_by('name')
    context = {
        'form': form,
        'categories': categories,
        'selected_category_id': category_id,
        'is_edit': False,
    }
    return render(request, 'catalog/admin_product_create.html', context)


@require_POST
def quick_order_checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    form = QuickWhatsAppOrderForm(request.POST)

    if form.is_valid():
        customer_name = form.cleaned_data['customer_name']
        customer_phone = form.cleaned_data['customer_phone']
        customer_email = form.cleaned_data.get('customer_email')
        digital_address = form.cleaned_data['digital_address']
        google_maps_url = form.cleaned_data.get('google_maps_url', '')
        quantity = form.cleaned_data.get('quantity', 1)
        delivery_notes = form.cleaned_data.get('delivery_notes', '')

        total_amount = product.price_ghs * quantity

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=customer_name,
            customer_email=customer_email or None,
            delivery_phone=customer_phone,
            digital_address=digital_address,
            google_maps_url=google_maps_url,
            delivery_notes=delivery_notes,
            total_amount_ghs=total_amount,
            status=Order.Status.PROCESSING,
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price_ghs=product.price_ghs,
        )

        # Build personalized WhatsApp message payload
        msg_lines = [
            f"Hello Wellful Home! My name is *{customer_name}*.",
            f"I have placed Order *#{order.order_number}* on your website for:",
            f"• *{product.name}* (Qty: {quantity}) - *GHS {total_amount:.2f}*",
            f"• *GhanaPost GPS / Location:* {digital_address}",
        ]
        if google_maps_url:
            msg_lines.append(f"• *Live Google Maps Pin:* {google_maps_url}")
        msg_lines.append(f"• *Contact Phone:* {customer_phone}")
        if customer_email:
            msg_lines.append(f"• *Email:* {customer_email}")
        if delivery_notes:
            msg_lines.append(f"• *Delivery Landmark / Notes:* {delivery_notes}")
        msg_lines.append("Please confirm product availability and dispatch time!")

        encoded_message = quote("\n".join(msg_lines))
        return redirect(f"https://wa.me/233268229696?text={encoded_message}")

    messages.error(request, "Please verify your delivery details and submit again.")
    return redirect('catalog:product_detail', slug=product.slug)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Handle deletion of an individual gallery image
    delete_img_id = request.POST.get('delete_gallery_image_id')
    if delete_img_id:
        ProductImage.objects.filter(id=delete_img_id, product=product).delete()
        messages.success(request, "Gallery photo removed.")
        return redirect('catalog:admin_product_edit', product_id=product.id)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save()
            gallery_files = request.FILES.getlist('gallery_images')
            current_count = product.gallery_images.count()
            available_slots = max(0, 10 - current_count)
            for img in gallery_files[:available_slots]:
                ProductImage.objects.create(product=updated_product, image=img)
            messages.success(request, f"Product '{updated_product.name}' was successfully updated!")
            return redirect('accounts:admin_dashboard')
    else:
        form = ProductCreateForm(instance=product)

    categories = Category.objects.all().order_by('name')
    context = {
        'form': form,
        'product': product,
        'categories': categories,
        'is_edit': True,
    }
    return render(request, 'catalog/admin_product_create.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@require_POST
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    try:
        product.delete()
        messages.success(request, f"Product '{product_name}' was removed from the catalog.")
    except ProtectedError:
        messages.error(
            request, 
            f"Cannot delete '{product_name}' because it is linked to completed customer orders. Deselect 'Active on Storefront' to hide it instead."
        )
    return redirect('accounts:admin_dashboard')