from django.urls import path
from .views import *
# # recent changes
# from users.views import ResetPasswordView


urlpatterns = [
<<<<<<< HEAD
    # Home
=======
    # # recent changes
    # path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
>>>>>>> f19ec8b970afadf0b0c50b8f5f6c4de75fe06798
    path('', index, name='index'),

    # Authentication
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('email-verify/', email_verify, name='email_verify'),
<<<<<<< HEAD

    # Forgot Password Flow
=======
    #  recent changes
>>>>>>> f19ec8b970afadf0b0c50b8f5f6c4de75fe06798
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('forgot-otp-verify/', forgot_otp_verify, name='forgot_otp_verify'),
    path('reset-password/', reset_password, name='reset_password'),

    # Static Pages
    path('about/', about, name='about'),
    path('delivery/', delivery, name='delivery'),
    path('sr/', sr, name='sr'),
    path('discount/', discount, name='discount'),
    path('hour/', hour, name='hour'),
    path('contact/', contact, name='contact'),
    path('categories/', categories, name='categories'),

    # Product Pages
    path('product/', product, name='product'),
    path('product-details/<uuid:product_id>/', product_details, name='product_details'),
<<<<<<< HEAD

    # Cart
    path('cart/', cart_list, name='cart_list'),
    path('cart/add/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/buy/<uuid:product_id>/', buy, name='buy'),
    path('cart/update/<uuid:cart_id>/', update_cart_item, name='update_cart'),
    path('cart/delete/<uuid:cart_id>/', delete_cart_item, name='delete_cart'),

    # Orders
    path('orders/', order_list, name='order_list'),
    path('orders/create/', create_order, name='create_order'),
    path('order-detail/<uuid:order_id>/', order_detail, name='order_detail'),

    # Checkout
    path('checkout/', checkout, name='checkout'),
    path('checkout/pay/<int:amt>/', pay, name='pay'),
    path('buy-now/<uuid:product_id>/', buy_now, name='buy_now'),

    # Profile & Address
    path('profile/', profile, name='profile'),
    path('add-address/', add_address, name='add_address'),

    # Category
    path('category/<str:category_name>/', category_view, name='category_view'),

    # Search 
    path('search/', product_search, name='product_search'),
    
]
=======
    path('cart/', cart_list, name='cart_list'),
    path('cart/add/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/add/<uuid:product_id>/', buy, name='buy'),
    path('cart/update/<uuid:cart_id>/', update_cart_item, name='update_cart'),
    path('cart/delete/<uuid:cart_id>/', delete_cart_item, name='delete_cart'),
    path('orders/', order_list, name='order_list'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<uuid:order_id>/', order_detail, name='order_detail'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/pay/<int:amt>/', pay, name='pay'),
    path('profile/', profile, name='profile'),
    path('add-address/', add_address, name='add_address'),
    path('category/<str:category_name>/', category_view, name='category_view'),
]
>>>>>>> f19ec8b970afadf0b0c50b8f5f6c4de75fe06798
