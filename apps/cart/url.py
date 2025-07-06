from django.urls import path
from .views import AddToCartAPIView,CartDetailAPIView,ClearCartAPIView

urlpatterns = [
    path('add_update/', AddToCartAPIView.as_view(), name='update-create-cart'),
    path('get/', CartDetailAPIView.as_view(), name='get-cart'),
    path('delete/', ClearCartAPIView.as_view(), name='delete-cart'),

]