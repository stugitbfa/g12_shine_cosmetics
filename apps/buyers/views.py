from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .helpers import *
from .models import Customer

import random
# Create your views here.
def index(request):
    return render(request, 'buyers/index.html')

def contact(request):
    return render(request, 'buyers/contact.html')

def shop(request):
    return render(request, 'buyers/shop.html')

def about(request):
    return render(request, 'buyers/about.html')

def signup(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']
        
        new_customer = Customer.objects.create(
            email=email_,
            mobile=mobile_,
            password=password_,
        )
        new_customer.save()
        print("Your registration successfully done. please check you rmail for mail conformation")
        return redirect('login')
        
    return render(request, 'buyers/signup.html')

def signup(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        if not is_email_verified(email_):
            print("Invaild Email")
            return redirect('signup')
        
        if Customer.objects.filter(email=email_).exists():
            print("Email already exist")
            return redirect('signup')
        
        if not is_valid_mobile_number(mobile_):
            print("Invaild Mobile number")
            return redirect('signup')
        
        if password_ != confirm_password_:
            print("Password and confirm password does't match.") 
            return redirect('signup')
    
        
        if not validate_password(password_)[0]:
            print(validate_password(password_)[1])
            return redirect('signup')
        
        new_customer = Customer.objects.create(
            email=email_,
            mobile=mobile_,
            password=password_
        )
        new_customer.save()
        send_mail("Confirm you account|Jadoo", f"OTP: {random.randint(111111, 999999)}", settings.EMAIL_HOST_USER, [f"{email_}"])
        print("Your registration successfully done. please check you rmail for mail conformation")
        return redirect('login')
        
    return render(request, 'buyers/signup.html')
def login(request):
    return render(request, 'buyers/login.html')


