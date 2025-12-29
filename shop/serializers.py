from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Cart, CartItem, Discount, Order, OrderItem, Product, Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_superuser"]
        read_only_fields = ["id", "is_superuser"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "avatar"]
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict[str, Any]):
        """Create a new user using Django's built-in helper.

        Return type is intentionally left un-annotated to avoid issues with
        dynamic user model typing in some analyzers.
        """
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )


class DiscountSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ["id", "percentage", "start_date", "end_date", "is_active", "created_at"]
        read_only_fields = ["id", "is_active", "created_at"]

    def get_is_active(self, obj: Discount) -> bool:
        return obj.is_active


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    discounts = DiscountSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "discount_percentage",
            "final_price",
            "stock_quantity",
            "is_available",
            "image",
            "created_at",
            "discounts",
        ]
        read_only_fields = ["id", "final_price", "is_available", "created_at"]

    def get_final_price(self, obj: Product) -> Decimal:
        return obj.final_price


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source="product"
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "subtotal",
        ]
        read_only_fields = ["id", "subtotal", "product"]

    def get_subtotal(self, obj: CartItem) -> Decimal:
        return obj.subtotal


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price", "created_at", "updated_at"]
        read_only_fields = ["id", "items", "total_price", "created_at", "updated_at"]

    def get_total_price(self, obj: Cart) -> Decimal:
        return obj.total_price


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source="product"
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "price_at_purchase",
            "subtotal",
        ]
        read_only_fields = ["id", "price_at_purchase", "subtotal", "product"]

    def get_subtotal(self, obj: OrderItem) -> Decimal:
        return obj.subtotal


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_items",
            "total_price",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "user", "total_price", "created_at"]

    def validate_order_items(self, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        items_data = self.initial_data.get("order_items") or []
        if not items_data:
            raise serializers.ValidationError({"order_items": "Order must contain at least one item."})

        # Ensure sufficient stock for each product
        for item in items_data:
            product = Product.objects.get(pk=item["product_id"])
            quantity = int(item["quantity"])
            if quantity <= 0:
                raise serializers.ValidationError({"order_items": "Quantity must be positive."})
            if product.stock_quantity < quantity or not product.is_available:
                raise serializers.ValidationError(
                    {"order_items": f"Insufficient stock for product {product.name}."}
                )
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> Order:
        request = self.context.get("request")
        assert request is not None
        user = request.user
        items_data = self.validated_data.get("order_items", [])

        total = Decimal("0.00")
        order = Order.objects.create(user=user, total_price=Decimal("0.00"))

        for item in items_data:
            product: Product = item["product"]
            quantity = int(item["quantity"])
            price_at_purchase = product.final_price
            total += price_at_purchase * quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price_at_purchase,
            )

        order.total_price = total.quantize(Decimal("0.01"))
        order.save(update_fields=["total_price"])

        # Cart cleanup (optional): if "clear_cart" flag is passed, clear user's cart
        clear_cart = self.context.get("clear_cart", False)
        if clear_cart and hasattr(user, "cart"):
            user.cart.items.all().delete()

        return order
