from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Cart, CartItem, Order, Product
from .permissions import IsOwnerOrSuperAdmin, IsSuperAdmin, IsSuperAdminOrReadOnly
from .serializers import (
    CartSerializer,
    OrderSerializer,
    ProductSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Any:  # type: ignore[override]
        return self.request.user


class ProfileAvatarView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self) -> Any:  # type: ignore[override]
        return self.request.user.profile


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

    def get_queryset(self):  # type: ignore[override]
        qs = Product.objects.all().select_related()

        params = self.request.query_params
        flt = (params.get("filter") or "").lower()
        sort = (params.get("sort") or "").lower()
        query = (params.get("q") or "").strip()

        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))

        # Filter logic
        if flt == "deals":
            qs = qs.filter(discount_percentage__gt=0)
        elif flt == "new":
            # Treat products created in the last 30 days as "new arrivals"
            cutoff = timezone.now() - timezone.timedelta(days=30)
            qs = qs.filter(created_at__gte=cutoff)
        elif flt == "best":
            # Simple heuristic for "best sellers": highest discount then stock
            qs = qs.order_by("-discount_percentage", "-stock_quantity")

        # Sorting logic
        if sort == "price_low":
            qs = qs.order_by("price")
        elif sort == "price_high":
            qs = qs.order_by("-price")
        elif sort == "newest":
            qs = qs.order_by("-created_at")
        elif not flt:
            # Default ordering when no explicit filter/sort: newest first
            qs = qs.order_by("-created_at")

        return qs


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperAdmin]

    def get_queryset(self):  # type: ignore[override]
        user = self.request.user
        qs = Order.objects.all().prefetch_related("order_items__product")
        if user.is_superuser:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer: OrderSerializer) -> None:  # type: ignore[override]
        serializer.save()


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_or_create_cart(self, user) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        cart = self._get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add")
    def add(self, request):
        cart = self._get_or_create_cart(request.user)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        if quantity <= 0:
            return Response({"detail": "Quantity must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id, is_available=True)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="remove")
    def remove(self, request):
        cart = self._get_or_create_cart(request.user)
        product_id = request.data.get("product_id")
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="update-quantity")
    def update_quantity(self, request):
        cart = self._get_or_create_cart(request.user)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        if quantity <= 0:
            return Response({"detail": "Quantity must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.quantity = quantity
        item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
