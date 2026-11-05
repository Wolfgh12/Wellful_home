from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pillar_type', 'slug', 'product_count')
    list_filter = ('pillar_type',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Total Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image_thumbnail',
        'name',
        'category',
        'sku',
        'price_ghs',
        'stock_quantity',
        'is_active',
        'is_featured',
    )
    list_filter = ('category', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    list_editable = ('price_ghs', 'stock_quantity', 'is_active', 'is_featured')
    list_per_page = 20

    fieldsets = (
        ("Pillar & Categorization", {
            'fields': ('category', 'sku', 'name', 'slug')
        }),
        ("Product Media", {
            'fields': ('image', 'image_preview'),
            'description': "Upload high-resolution photography for this item."
        }),
        ("Pricing & Stock Levels", {
            'fields': ('price_ghs', 'stock_quantity', 'is_active', 'is_featured')
        }),
        ("Description & Technical Specs", {
            'fields': ('description', 'specifications'),
            'description': 'Input specifications as JSON key-value pairs (e.g. {"Weight": "15 kg", "Material": "Steel"}).'
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: contain; border-radius: 8px; border: 1px solid #e5e7eb;" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af; font-size: 11px;">No Image</span>')
    image_thumbnail.short_description = "Thumbnail"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 250px; object-fit: contain; border-radius: 12px; border: 1px solid #d1d5db;" />',
                obj.image.url
            )
        return "Upload an image and save to see preview."
    image_preview.short_description = "Current Preview"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price_ghs', 'subtotal_ghs')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'delivery_phone', 'digital_address', 'total_amount_ghs', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username', 'delivery_phone', 'digital_address')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]