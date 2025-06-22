from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('email-verify/', email_verify, name='email_verify'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('categories/', categories, name='categories'),
    path('product/', product, name='product'),
    path('product-details/<uuid:product_id>', product_details, name='product_details'),
    path('cart/', cart, name='cart'),
    path('profile/', profile, name='profile'),
    path('category/<str:category_name>/', category_view, name='category_view'),

]