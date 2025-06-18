from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

from .helpers import *
from .models import Customer

from functools import wraps

import random

# Create your views here.

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'customer_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper 

def login(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_ = request.POST['password']

        if not Customer.objects.filter(email=email_).exists():
            print("Email does't Exist")
            return redirect('login')

        get_customer = Customer.objects.get(email=email_)

        if not get_customer.is_active:
            print("you account is deactivate please contact to customer care.")
            return redirect('login')

        is_valid = check_password(password_, get_customer.password)
        if not is_valid:
            print("Email or paddword not match.")
            return redirect('login')
        
        request.session['customer_id'] = str(get_customer.tid)
        return redirect('index')
        
    return render(request, 'buyers/login.html' \
    '')

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
            password=make_password(password_)
        )
        new_customer.save()
        otp = random.randint(111111, 999999)
        new_customer.otp = otp
        new_customer.save()
        subject = "Confirm Your Account | Jadoo"
        message = f"""
        Dear User,

        Thank you for registering with Jadoo.

        Your One-Time Password (OTP) for email verification is: {otp}

        Please enter this OTP in the app/website to complete your email verification process. 

        If you did not request this, please ignore this email.

        Best regards,  
        Team Jadoo
        """

        send_mail(subject, message, settings.EMAIL_HOST_USER, [f"{email_}"])
        print("Your registration successfully done. please check you rmail for mail conformation")
        context = {
            'email': email_
        }
        return render(request, 'buyers/email_verify.html', context)

    return render(request, 'buyers/signup.html')

def email_verify(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']

        if not Customer.objects.filter(email=email_).exists():
            print("Email does't Exixt")
            return render(request, 'buyers/email_verify.html', {'email': email_})
        
        get_customer = Customer.objects.get(email=email_)

        if otp_ != get_customer.otp:
            print("Invalid OTP")
            return render(request, 'buyers/email_verify.html', {'email': email_})
        
        get_customer.is_active = True
        get_customer.save()
        return redirect('login')

    return render(request, 'buyers/email_verify.html')

def index(request):
    return render(request, 'buyers/index.html')

def about(request):
    return render(request, 'buyers/about.html')

def shop(request):
    return render(request, 'buyers/shop.html')

def contact(request):
    return render(request, 'buyers/contact.html')


def blogs(request):
    return render(request, 'buyers/blogs.html')

@login_required
def profile(request):
    return render(request, 'buyers/profile.html')

@login_required
def logout(request):
    del request.session['customer_id']
    print("Now, you are logged Out.")
    return redirect('login')