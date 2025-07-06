from django.urls import path
from .views import ProductDetailAPIView,ProductListAPIView,ProductReviewAPIView

urlpatterns = [
    path('api/products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/products/<int:product_id>/reviews/', ProductReviewAPIView.as_view(), name='product-review'),
]