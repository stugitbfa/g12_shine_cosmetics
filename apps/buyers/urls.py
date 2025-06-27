from django.urls import path
from .views import *
# # recent changes
# from users.views import ResetPasswordView


urlpatterns = [
    # # recent changes
    # path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('email-verify/', email_verify, name='email_verify'),
    #  recent changes
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('categories/', categories, name='categories'),
    path('product/', product, name='product'),
    path('product-details/<uuid:product_id>/', product_details, name='product_details'),
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
