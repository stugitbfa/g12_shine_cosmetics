from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, time as dt_time
import random
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decimal import Decimal
import razorpay

client = razorpay.Client(auth=(settings.RZP_KEY_ID, settings.RZP_KEY_SECRET))

from .models import *

# Decorator to require login
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

        # Check if user exists
        if not Customer.objects.filter(email=email_).exists():
            messages.error(request, "Email doesn't exist.")
            return redirect('login')

        get_customer = Customer.objects.get(email=email_)

        # Check if account is active
        if not get_customer.is_active:
            messages.error(request, "Account is inactive. Contact support.")
            return redirect('login')

        # Check password
        if not check_password(password_, get_customer.password):
            messages.error(request, "Incorrect password.")
            return redirect('login')

        # Successful login
        request.session['is_logged_in'] = True
        request.session['customer_id'] = str(get_customer.tid)
        messages.success(request, "Logged in successfully!")
        return redirect('index')

    return render(request, 'buyers/login.html')

def signup(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        # ✅ Check if email already exists
        if Customer.objects.filter(email=email_).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        # ✅ Check if passwords match
        if password_ != confirm_password_:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # ✅ Create new customer
        new_customer = Customer.objects.create(
            email=email_,
            mobile=mobile_,
            password=make_password(password_)
        )

        # ✅ Generate and save OTP
        otp = random.randint(111111, 999999)
        new_customer.otp = str(otp)
        new_customer.save()

        # ✅ Send OTP email
        subject = "Confirm Your Account | SHINE Cosmetics"
        message = f"""
Dear User,

Thank you for registering with SHINE Cosmetics.

Your OTP for email verification is: {otp}

Please enter this OTP to complete verification.

Best regards,  
Team SHINE Cosmetics
"""
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email_])

        messages.success(request, "Registration successful! Check your email for OTP.")
        return render(request, 'buyers/email_verify.html', {'email': email_})

    return render(request, 'buyers/signup.html')

def email_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        try:
            customer = Customer.objects.get(email=email)
            if otp == customer.otp:
                customer.otp = ''
                customer.save()
                messages.success(request, "OTP verified. Please login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP.")
        except Customer.DoesNotExist:
            messages.error(request, "Invalid email.")
        return render(request, 'buyers/email_verify.html', {'email': email})

    return redirect('signup')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            customer = Customer.objects.get(email=email)
            otp = random.randint(111111, 999999)
            customer.otp = str(otp)
            customer.save()

            subject = "Password Reset OTP | SHINE Cosmetics"
            message = f"""
Dear User,

You requested to reset your password for SHINE Cosmetics.

Your OTP for password reset is: {otp}

Please enter this OTP to proceed.

Best regards,  
Team SHINE Cosmetics
"""
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            messages.success(request, "OTP sent to your email.")
            return redirect(f'/forgot-otp-verify/?email={email}')

        except Customer.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forgot_password')

    return render(request, 'buyers/forgot_password.html')

def forgot_otp_verify(request):
    email = request.GET.get('email') or request.POST.get('email')

    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            customer = Customer.objects.get(email=email)
            if otp == customer.otp:
                customer.otp = ''
                customer.save()
                
                # ✅ Store verified email in session to avoid passing in URL
                request.session['reset_email'] = email

                messages.success(request, "OTP verified. Set your new password.")
                return redirect('reset_password')

            else:
                messages.error(request, "Invalid OTP.")

        except Customer.DoesNotExist:
            messages.error(request, "Invalid email.")

    return render(request, 'buyers/forgot_otp_verify.html', {'email': email})

def reset_password(request):
    email = request.session.get('reset_email')

    if not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'buyers/reset_password.html')

        try:
            customer = Customer.objects.get(email=email)
            customer.password = make_password(password)
            customer.save()

            # ✅ Clear session email after reset
            del request.session['reset_email']

            messages.success(request, "Password reset successfully. Please login.")
            return redirect('login')

        except Customer.DoesNotExist:
            messages.error(request, "Invalid email.")
            return redirect('forgot_password')

    return render(request, 'buyers/reset_password.html')

def index(request):
    return render(request, 'buyers/index.html')

def about(request):
    return render(request, 'buyers/about.html')
def discount(request):
    return render(request, 'buyers/discount.html')

def hour(request):
    return render(request, 'buyers/hour.html')

def delivery(request):
    return render(request, 'buyers/delivery.html')

def sr(request):
    return render(request, 'buyers/sr.html')

def categories(request):
    return render(request, 'buyers/category.html')

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

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        messages.success(request, "Message sent successfully!")
        return redirect('contact')

    return render(request, 'buyers/contact.html')

@login_required
def cart_list(request):
    customer = request.session['customer_id'] # or use session
    cart_items = Cart.objects.filter(customer=customer)
    total = sum(item.total_amount for item in cart_items)
    return render(request, 'buyers/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def buy(request, product_id):
    customer = get_object_or_404(Customer, tid=request.session.get('customer_id'))
    product = get_object_or_404(Product, tid=product_id)

    cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {product.title} to cart.")
    return redirect('cart_list')
    
@login_required
def add_to_cart(request, product_id):
    customer = get_object_or_404(Customer, tid=request.session.get('customer_id'))
    product = get_object_or_404(Product, tid=product_id)

    cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"✅ {product.title} added to your cart.")
    return redirect('product')  # Redirect back to product page
    
@login_required
def update_cart_item(request, cart_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(Cart, tid=cart_id)

        if quantity <= 0:
            cart_item.delete()
            messages.info(request, "Item removed from cart.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")

    return redirect('cart_list')

@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, tid=cart_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_list')

@login_required
def checkout(request):
    customer_id = request.session.get('customer_id')
    customer = get_object_or_404(Customer, tid=customer_id)
    cart_items = Cart.objects.filter(customer=customer)

    if not cart_items.exists():
        return redirect('cart_list')

    addresses = Address.objects.filter(customer=customer)
    primary_address = addresses.filter(is_primary=True).first()

    total = sum(item.total_amount for item in cart_items)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checkout.")
        return redirect('cart_list')

    return render(request, 'buyers/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'addresses': addresses,
        'primary_address': primary_address,
    })

@login_required
def order_list(request):
    customer = get_object_or_404(Customer, tid=request.session.get('customer_id'))
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    return render(request, 'buyers/order_list.html', {'orders': orders})

@login_required
def create_order(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        customer = get_object_or_404(Customer, tid=customer_id)
        cart_items = Cart.objects.filter(customer=customer)

        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        delivery_type = request.POST.get('delivery_type')
        delivery_date_str = request.POST.get('delivery_date')
        delivery_time_str = request.POST.get('delivery_time')

        tomorrow = timezone.now().date() + timedelta(days=1)
        total = sum(item.total_amount for item in cart_items)

        # Defaults
        delivery_date = None
        delivery_time = None

        if delivery_type == 'urgent':
            try:
                delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
                delivery_time = datetime.strptime(delivery_time_str, '%H:%M').time()
            except Exception:
                messages.error(request, "Urgent delivery requires valid date and time.")
                return redirect('checkout')

            if delivery_date < tomorrow:
                messages.error(request, "Urgent delivery must be scheduled from tomorrow.")
                return redirect('checkout')

            if not (dt_time(8, 0) <= delivery_time <= dt_time(20, 0)):
                messages.error(request, "Urgent delivery time must be between 08:00 AM and 08:00 PM.")
                return redirect('checkout')

            total += Decimal('49.00')   # Add urgent charge

        elif delivery_type == 'scheduled':
            # Random delivery date between 2 to 5 days from today
            random_days = randint(2, 5)
            delivery_date = timezone.now().date() + timedelta(days=random_days)

        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            address=address,
            payment_method=payment_method,
            delivery_type=delivery_type,
            delivery_date=delivery_date,
            delivery_time=delivery_time
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        if delivery_type == 'urgent':
            messages.success(request, "Urgent order placed with ₹49.00 extra charge.")
        else:
            messages.success(request, "Scheduled order placed successfully!")

        # Order Confirmation Email (HTML)
        subject = f"Order Confirmation - Order #{order.tid} | SHINE Cosmetics"
        from_email = settings.EMAIL_HOST_USER
        to_email = [customer.email]

        html_content = render_to_string('buyers/order_pdf.html', {
            'order': order,
            'customer': customer
        })

        text_content = f"Thank you for your order #{order.tid} with SHINE Cosmetics."

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

        return redirect('order_list')

@login_required
def order_detail(request, order_id):
    customer = get_object_or_404(Customer, tid=request.session.get('customer_id'))
    order = get_object_or_404(Order, tid=order_id, customer=customer)
    order_items = order.order_items.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'buyers/order_detail.html', context)


@login_required
def profile(request):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        messages.error(request, "Please login to access your profile.")
        return redirect('login')

    try:
        customer = Customer.objects.get(tid=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found. Please login again.")
        return redirect('logout')

    try:
        primary_address = Address.objects.get(customer=customer, is_primary=True)
    except Address.DoesNotExist:
        primary_address = None

    context = {
        'customer': customer,
        'primary_address': primary_address,
        'has_primary': primary_address is not None
    }
    return render(request, 'buyers/profile.html', context)

def product(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'buyers/product.html', {'page_obj': page_obj})

def product_details(request, product_id):
    product = get_object_or_404(Product, tid=product_id)
    return render(request, 'buyers/product_details.html', {'product': product})

# Payment view stub (depends on your payment gateway)
@login_required
def pay(request, amt):
    # Setup payment logic with your gateway here
    # For now, just a placeholder render
    return render(request, 'buyers/payment.html', {'amount': amt})

@login_required
def add_address(request):
    if request.method == 'POST':
        customer_id = request.session['customer_id']
        customer = get_object_or_404(Customer, tid=customer_id)

        # If "Set as Primary" is checked, clear existing primary addresses
        if request.POST.get('is_primary') == 'on':
            Address.objects.filter(customer=customer, is_primary=True).update(is_primary=False)

        Address.objects.create(
            customer=customer,
            full_name=request.POST['full_name'],
            mobile=request.POST['mobile'],
            pincode=request.POST['pincode'],
            house_no=request.POST['house_no'],
            area_street=request.POST['area_street'],
            landmark=request.POST.get('landmark', ''),
            city=request.POST['city'],
            state=request.POST['state'],
            country=request.POST['country'],
            is_primary=True if request.POST.get('is_primary') == 'on' else False,
        )
        messages.success(request, "Address added successfully.")

        return redirect('profile')

@login_required
def buy_now(request, product_id):
    customer = get_object_or_404(Customer, tid=request.session.get('customer_id'))
    product = get_object_or_404(Product, tid=product_id)

    # OPTIONAL: Clear existing cart items if Buy Now should only process this product
    Cart.objects.filter(customer=customer).delete()

    # Add this product with quantity 1
    Cart.objects.create(customer=customer, product=product, quantity=1)

    # Redirect to checkout
    return redirect('checkout')

def product_search(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(is_available=True)

    if query:
        products = products.filter(title__icontains=query)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    products = products.order_by('-created_at')

    return render(request, 'buyers/product_search.html', {
        'products': products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    })

@login_required
def logout(request):
    del request.session['customer_id']
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')