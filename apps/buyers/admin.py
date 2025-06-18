from django.contrib import admin
from .models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['tid', 'email', 'mobile', 'is_active']
    list_filter = ['is_active']
    list_editable = ['mobile', 'is_active']
    search_fields = ['email', 'mobile']
    list_per_page = 50
admin.site.register(Customer, CustomerAdmin)
