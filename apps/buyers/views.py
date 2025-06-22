from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from .models import *
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
        subject = "Confirm Your Account | SHINE Cosmetics"
        message = f"""
        Dear User,

        Thank you for registering with SHINE Cosmetics.

        Your One-Time Password (OTP) for email verification is: {otp}

        Please enter this OTP in the website to complete your email verification process. 

        If you did not request this, please ignore this email.

        Best regards,  
        Team SHINE Cosmetics
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
def forgot_password(request):
    return render(request, 'buyers/forgot_password.html')
def otp_verification(request):
    return render(request, 'buyers/otp_verification.html')
def index(request):
    return render(request, 'buyers/index.html')
def about(request):
    return render(request, 'buyers/about.html')
from django.contrib import messages  

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        user_message = request.POST['message']  

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=user_message
        )

        messages.success(request, "Your message has been sent successfully! Our team will get back to you shortly.") 
        return redirect('contact')

    return render(request, 'buyers/contact.html')

def product(request):
    
    product_list = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    
    # Paginate with 6 products per page
    paginator = Paginator(product_list, 9)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories':categories
    }
    return render(request, 'buyers/product.html', context)

def product_details(request, product_id):
    product = get_object_or_404(Product, tid=product_id)
    context = {
        'product':product
    }
    print(product)
    return render(request, 'buyers/product_details.html', context)
def category_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category, is_available=True).order_by('-created_at')

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'buyers/category_template.html', {
        'category': category.name,
        'products': page_obj,
        'page_obj': page_obj,
    })

def categories(request):
    return render(request, 'buyers/categories.html')

def cart(request):
    return render(request, 'buyers/cart.html')
def profile(request):
    return render(request, 'buyers/profile.html')