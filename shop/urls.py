from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CartViewSet,
    OrderViewSet,
    ProductViewSet,
    ProfileAvatarView,
    ProfileView,
    RegisterView,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/me/", ProfileView.as_view(), name="auth-me"),
    path("auth/profile/", ProfileAvatarView.as_view(), name="auth-profile"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API resources
    path("", include(router.urls)),
]
