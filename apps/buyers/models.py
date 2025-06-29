from django.db import models
import uuid
from datetime import timedelta, date
import random

class BaseModel(models.Model):
    tid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Customer(BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    otp = models.CharField(max_length=10, default='112233')
    is_active = models.BooleanField(default=True)

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    house_no = models.CharField(max_length=255)
    area_street = models.TextField()
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    is_primary = models.BooleanField(default=False)  # Marks this as the default address

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_primary', '-updated_at']  # Primary ones appear first

    def __str__(self):
        return f"{self.full_name}, {self.city} - {self.pincode}"

    def save(self, *args, **kwargs):
        # Ensure only one primary address per customer
        if self.is_primary:
            Address.objects.filter(customer=self.customer, is_primary=True).update(is_primary=False)
        super(Address, self).save(*args, **kwargs)

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

CONTACT_STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]

class ContactMessage(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=CONTACT_STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"

class Cart(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('customer', 'product')

    @property
    def total_amount(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self):
        return f"{self.customer.email} - {self.product.title} ({self.quantity})"

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

class Order(BaseModel):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    address = models.TextField()
    payment_method = models.CharField(max_length=100, default='COD')  # COD, UPI, etc.

    delivery_type = models.CharField(max_length=20, default='scheduled')  # scheduled or urgent
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-assign random delivery date between 2 to 5 days for scheduled deliveries
        if self.delivery_type == 'scheduled' and not self.delivery_date:
            days_to_add = random.randint(2, 5)
            self.delivery_date = date.today() + timedelta(days=days_to_add)

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.tid} - {self.customer.email}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at purchase time

    @property
    def total_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

# class OrderItem(BaseModel):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of purchase

#     @property
#     def total_price(self):
#         return round(self.price * self.quantity, 2)

#     def __str__(self):
#         return f"{self.product.title} x {self.quantity}"

# CONTACT_STATUS_CHOICES = [
#     ('new', 'New'),
#     ('in_progress', 'In Progress'),
#     ('resolved', 'Resolved'),
# ]

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at purchase time

    @property
    def total_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

