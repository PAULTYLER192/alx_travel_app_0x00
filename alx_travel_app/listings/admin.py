from django.contrib import admin
from .models import Listing, Booking, Review, Amenity

# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'host', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'check_in', 'check_out')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'rating')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)