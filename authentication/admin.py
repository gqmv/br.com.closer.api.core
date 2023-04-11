from django.contrib import admin
from .models import CustomUser


class CustomUserAdminConfig(admin.ModelAdmin):
    ordering = ("first_name",  "tax_id")
    list_display = ("first_name",  "tax_id", "phone_number")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("first_name",  "tax_id",  "phone_number")
    
    fieldsets = (
        (None, {"fields": ("first_name", "tax_id",  "phone_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )
    

# Register your models here.
admin.site.register(CustomUser, CustomUserAdminConfig)
