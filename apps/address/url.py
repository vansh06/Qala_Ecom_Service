from .views import AddressListCreateView
from django.urls import path 

urlpatterns =[
     path('add_address/', AddressListCreateView.as_view(), name="logout"),

]