from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review, Amenity
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, reviews, and amenities'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Clear existing data (optional, comment out if you want to keep existing data)
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        Amenity.objects.all().delete()
        User.objects.exclude(username='airbnb_user').delete()

        # Create sample users
        users = []
        for i in range(3):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password123'
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS('Created 3 users'))

        # Create sample amenities
        amenities_data = ['WiFi', 'Kitchen', 'Parking', 'Air Conditioning', 'Pool']
        amenities = [Amenity.objects.create(name=name) for name in amenities_data]
        self.stdout.write(self.style.SUCCESS('Created 5 amenities'))

        # Create sample listings
        listings_data = [
            {'title': 'Cozy Nairobi Apartment', 'city': 'Nairobi', 'price': 50.00, 'description': 'A cozy apartment in the heart of Nairobi'},
            {'title': 'Mombasa Beach House', 'city': 'Mombasa', 'price': 120.00, 'description': 'Beachfront house with stunning views'},
            {'title': 'Kisumu Lake Cottage', 'city': 'Kisumu', 'price': 80.00, 'description': 'Charming cottage by Lake Victoria'},
        ]
        listings = []
        for data in listings_data:
            listing = Listing.objects.create(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                city=data['city'],
                host=random.choice(users)
            )
            # Assign random amenities
            listing.amenities.set(random.sample(amenities, k=random.randint(2, 4)))
            listings.append(listing)
        self.stdout.write(self.style.SUCCESS('Created 3 listings'))

        # Create sample bookings
        for listing in listings:
            for i in range(2):
                check_in = timezone.now().date() + timedelta(days=random.randint(1, 30))
                check_out = check_in + timedelta(days=random.randint(1, 5))
                total_price = listing.price * (check_out - check_in).days
                Booking.objects.create(
                    property=listing,
                    guest=random.choice(users),
                    check_in=check_in,
                    check_out=check_out,
                    total_price=total_price
                )
        self.stdout.write(self.style.SUCCESS('Created 6 bookings'))

        # Create sample reviews
        for listing in listings:
            for i in range(2):
                Review.objects.create(
                    property=listing,
                    guest=random.choice(users),
                    rating=random.randint(1, 5),
                    comment=f'Review {i+1} for {listing.title}'
                )
        self.stdout.write(self.style.SUCCESS('Created 6 reviews'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))