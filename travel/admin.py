"""Django Admin configuration for Tourly models."""
from django.contrib import admin
from .models import User, Destination, TourPackage, Booking, ContactMessage


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'is_admin', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('is_admin', 'created_at')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'category')
    list_filter = ('category', 'country')
    search_fields = ('name', 'description', 'attractions')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'package_name', 'destination', 'duration', 'price', 'availability')
    list_filter = ('destination__category', 'destination')
    search_fields = ('package_name', 'description', 'hotel_info')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer_name', 'package', 'travel_date',
        'travelers', 'total_price', 'booking_status', 'created_at'
    )
    list_filter = ('booking_status', 'travel_date')
    search_fields = ('customer_name', 'customer_email', 'package__package_name')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
