"""django_eshop_dec_22 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from eshop import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('shop', views.shop, name='shop'),
    path('shop/<slug:cat>', views.shop, name='shop'),
    path('detail/<int:id>', views.detail, name="detail"),
    path('contact', views.contact, name="contact"),
    path('cart', views.cart, name="cart"),
    path('cart/decreace_increase', views.decreace_increase, name="decreace_increase"),
    path('coupons', views.coupons, name="coupons"),
    path('del_in_cart', views.del_in_cart, name="del_in_cart"),
    path('checkout', views.checkout, name="checkout"),
    path('proceedCheckout', views.proceedCheckout, name="proceedCheckout"),
    path('search', views.search, name='search'),
    path('', include('myauth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('edit_cart_item/<int:id_product>', views.edit_order_item, name='edit_cart_item'),
    path('like',views.like,name="like"),
    path('add_to_cart/',views.add_to_cart, name="add_to_cart")
    # path('products/<int:product_id>/like/', views.like_product, name='like_product'),
    # path('', include('admin_volt.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
