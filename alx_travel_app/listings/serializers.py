from rest_framework import serializers
from .models import Listing, Booking, Amenity
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price', 'city', 'host', 'amenities']
        read_only_fields = ['host']

    def create(self, validated_data):
        # Automatically set the host to the authenticated user
        validated_data['host'] = self.context['request'].user
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    property = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), source='property', write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'property', 'property_id', 'guest', 'check_in', 'check_out', 'total_price']
        read_only_fields = ['guest', 'total_price']

    def validate(self, data):
        # Ensure check_out is after check_in
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            property=data['property'],
            check_in__lt=data['check_out'],
            check_out__gt=data['check_in']
        )
        if overlapping_bookings.exists():
            raise serializers.ValidationError("This property is already booked for the selected dates.")

        # Calculate total_price based on property price and duration
        days = (data['check_out'] - data['check_in']).days
        if days <= 0:
            raise serializers.ValidationError("Booking duration must be at least one day.")
        data['total_price'] = data['property'].price * days
        return data

    def create(self, validated_data):
        # Automatically set the guest to the authenticated user
        validated_data['guest'] = self.context['request'].user
        return super().create(validated_data)