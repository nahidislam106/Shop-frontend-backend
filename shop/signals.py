from __future__ import annotations

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, Product, Profile

User = get_user_model()


@receiver(post_save, sender=OrderItem)
def reduce_stock_on_order_item_create(sender, instance: OrderItem, created: bool, **kwargs) -> None:
    """Reduce product stock when a new order item is created.

    Keeps logic simple by adjusting stock as soon as each OrderItem is saved
    for the first time.
    """

    if not created:
        return

    product: Product = instance.product
    if instance.quantity <= 0:
        return

    # Ensure stock doesn't go negative
    new_stock = max(0, product.stock_quantity - instance.quantity)
    product.stock_quantity = new_stock
    # Availability flag auto-updated in Product.save
    product.save(update_fields=["stock_quantity", "is_available"])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs) -> None:
    """Ensure each user has an associated profile."""

    if not created:
        return

    Profile.objects.create(user=instance)
