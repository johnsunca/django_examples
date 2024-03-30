from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:category_id>/', views.home, name='home'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/edit/<int:cart_item_id>/', views.edit_cart_item, name='edit_cart_item'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.create_order, name='create_order'),
    
    path('test_data/', views.test_data, name='test_data'),    
]
