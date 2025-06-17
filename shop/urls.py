from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import product_detail

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('api/add-to-cart/', views.api_add_to_cart, name='api_add_to_cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)