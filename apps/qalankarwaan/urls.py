"""
URL configuration for qalankarwaan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Qalakarwaan Administration'
admin.site.site_title = 'Qalakarwaan Administration'
admin.site.index_title = 'Qalakarwaan Administration'




urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('oauth.url')),  # Include app URLs
    path('address/', include('address.url')),  # Include app URLs
    path('product/', include('product.url')),  # Include app URLs
    path('cart/', include('cart.url')),
    path('orders/', include('orders.url'))



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
