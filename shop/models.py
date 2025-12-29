from __future__ import annotations

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Profile({self.user})"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Base discount percentage for the product.",
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name

    @property
    def active_discount_offer(self) -> "Discount | None":
        now = timezone.now()
        return (
            self.discounts.filter(
                models.Q(start_date__lte=now) | models.Q(start_date__isnull=True),
                models.Q(end_date__gte=now) | models.Q(end_date__isnull=True),
            )
            .order_by("-percentage")
            .first()
        )

    @property
    def final_price(self) -> Decimal:
        """Calculate final price with highest applicable discount."""
        discount = self.discount_percentage
        offer = self.active_discount_offer
        if offer and offer.percentage > discount:
            discount = offer.percentage
        if discount <= 0:
            return self.price
        return (self.price * (Decimal("100.00") - discount) / Decimal("100.00")).quantize(
            Decimal("0.01")
        )

    def save(self, *args, **kwargs) -> None:  # type: ignore[override]
        # Auto update availability based on stock
        self.is_available = self.stock_quantity > 0
        super().save(*args, **kwargs)


class Discount(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="discounts",
    )
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.percentage}% for {self.product}"

    @property
    def is_active(self) -> bool:
        now = timezone.now()
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Cart({self.user})"

    @property
    def total_price(self) -> Decimal:
        total = Decimal("0.00")
        for item in self.items.select_related("product"):
            total += item.subtotal
        return total.quantize(Decimal("0.01"))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.product} x {self.quantity}"

    @property
    def subtotal(self) -> Decimal:
        return (self.product.final_price * self.quantity).quantize(Decimal("0.01"))


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Order #{self.pk} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.product} x {self.quantity} (order {self.order_id})"

    @property
    def subtotal(self) -> Decimal:
        return (self.price_at_purchase * self.quantity).quantize(Decimal("0.01"))
