from django.contrib import admin
from .models import *
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['tid', 'email', 'mobile', 'is_active']
    list_filter = ['is_active']
    list_editable = ['mobile', 'is_active']
    search_fields = ['email', 'mobile']
    list_per_page = 50
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'subject', 'message']