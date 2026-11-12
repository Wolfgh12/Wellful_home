import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    PILLAR_CHOICES = [
        ('MEDICAL', 'Wellful Care'),
        ('DEPOSITORY', 'Wellful Data'),
        ('VOLTAGE', 'Wellful Devices'),
        ('FITNESS', 'Wellful Fitness'),
        ('SUPPLEMENTS', 'Wellful Food'),
        ('SANITARY', 'Wellful Sanitary'),
        ('FOOTWEAR', 'Wellful Sole'),
    ]

    class AvailabilityStatus(models.TextChoices):
        IN_STOCK = 'IN_STOCK', 'In Stock'
        STOCKING_SOON = 'STOCKING_SOON', 'Stocking Soon'
        COMING_SOON = 'COMING_SOON', 'Coming Soon'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    pillar_type = models.CharField(
        max_length=20,
        choices=PILLAR_CHOICES,
        unique=True,
        help_text="The core wellness pillar this category aligns with"
    )
    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.IN_STOCK,
        help_text="Controls whether this pillar shows In Stock, Stocking Soon, or Coming Soon (Locked)"
    )
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Image filename or Lucide icon class")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_locked(self):
        return self.availability_status == self.AvailabilityStatus.COMING_SOON

    @property
    def is_in_stock(self):
        return self.availability_status == self.AvailabilityStatus.IN_STOCK

    @property
    def is_stocking_soon(self):
        return self.availability_status == self.AvailabilityStatus.STOCKING_SOON

    def __str__(self):
        return f"{self.name} ({self.get_pillar_type_display()}) - {self.get_availability_status_display()}"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)
    description = models.TextField()
    specifications = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Key-value technical specs (e.g., voltage rating, grip rating, size)"
    )
    price_ghs = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Retail price in Ghanaian Cedis (GHS)"
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity <= 5

    @property
    def total_value(self):
        return self.price_ghs * self.stock_quantity

    def __str__(self):
        return f"{self.name} - GHS {self.price_ghs}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='gallery_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/gallery/%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Gallery image for {self.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Payment'
        PROCESSING = 'PROCESSING', 'Processing & Packaging'
        DISPATCHED = 'DISPATCHED', 'Out for Delivery'
        DELIVERED = 'DELIVERED', 'Delivered & Installed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    customer_name = models.CharField(max_length=150, blank=True)
    customer_email = models.EmailField(blank=True, null=True)
    delivery_phone = models.CharField(max_length=20)
    digital_address = models.CharField(max_length=100, help_text="GhanaPost GPS Address or Area Location")
    google_maps_url = models.URLField(max_length=500, blank=True, help_text="Live Google Maps GPS Pin")
    delivery_notes = models.TextField(blank=True)
    total_amount_ghs = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROCESSING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"WF-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.customer_name or (self.user.username if self.user else "Guest")
        return f"Order #{self.order_number} - {name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price_ghs = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal_ghs(self):
        return self.unit_price_ghs * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.order_number})"