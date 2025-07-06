from django.urls import path
from . import views
from .views import RegisterView,LoginAPIView,UserProfileView,AppUserLogoutView
from .views import AppUserTokenRefreshView

urlpatterns = [
    path('home/', views.home, name='home'),
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('get_current_user/', UserProfileView.as_view(), name='User_profile'),
    path('token/refresh/', AppUserTokenRefreshView.as_view(), name="token_refresh"),
    path('logout/', AppUserLogoutView.as_view(), name="logout"),


]
