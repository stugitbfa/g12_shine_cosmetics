from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('email-verify/', email_verify, name='email_verify'),
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('contact/', contact, name='contact'),
]