from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path("",index,name='index'),
   path("contact/",contact,name='contact'),
   path("about/",about,name='about'),
   path("shop/",shop,name='shop'),
   path("signup/",signup,name='signup'),
   path("login/",login,name='login'),
]