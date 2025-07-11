from email import message
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from .models import (Booking, ContactMessage, Customer, GalleryImage,DomesticTour,
                     Notification, SlideImage, TourPackage, UmraPackage,
                     VacationTour)

# === Branding the Admin Site ===
admin.site.site_header = "Yusra Tour & Travel Admin"
admin.site.site_title = "Yusra Admin Portal"
admin.site.index_title = "Welcome to Yusra Admin Dashboard"


# === Helper Functions ===
def is_admin(user):
    return user.groups.filter(name="Admin").exists() or user.is_superuser


def is_manager(user):
    return user.groups.filter(name="Manager").exists()


def is_manager_or_admin(user):
    return is_manager(user) or is_admin(user)


# === Model Admins ===


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "category", "price")
    search_fields = ("name", "country", "category")

    def has_view_permission(self, request, obj=None):
        return is_manager_or_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_manager_or_admin(request.user)

    def has_add_permission(self, request):
        return is_manager_or_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return False  # Disallow deletion for everyone


@admin.register(UmraPackage)
class UmraPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "price", "available_from")
    search_fields = ("name", "country")
    list_filter = ("country", "available_from")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'subject', 'sent_at'] 
    search_fields = ("name", "email","phone_number", "subject", "message")
    list_filter = ("sent_at",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer", "package", "date", "status")
    search_fields = ("customer__name", "package__name")
    list_filter = ("status", "date")

    def has_module_permission(self, request):
        return is_manager_or_admin(request.user)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "target_group", "created_at")
    search_fields = ("title", "message", "target_group")
    list_filter = ("target_group", "created_at")


# === Simple Model Registrations ===
admin.site.register(VacationTour)
admin.site.register(DomesticTour)
admin.site.register(GalleryImage)
admin.site.register(SlideImage)


# === Override User Admin ===
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def has_module_permission(self, request):
        return is_manager_or_admin(request.user)

    def has_view_permission(self, request, obj=None):
        return is_manager_or_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_manager_or_admin(request.user)

    def has_add_permission(self, request):
        return is_manager_or_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)  # Only Admin can delete users


# === Override Group Admin ===
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return is_manager_or_admin(request.user)

    def has_view_permission(self, request, obj=None):
        return is_manager_or_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_manager_or_admin(request.user)

    def has_add_permission(self, request):
        return is_manager_or_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)  # Only Admin can delete groups


