from django.urls import path
from .views import CreateOrderView,RazorpayVerifyView

urlpatterns = [

    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('verify-payment/', RazorpayVerifyView.as_view(), name='verfiy-payment'),



]
