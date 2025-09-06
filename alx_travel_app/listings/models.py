from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    city = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    amenities = models.ManyToManyField(Amenity, related_name='listings')

    def __str__(self):
        return self.title

class Booking(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.property.title} by {self.guest.username}"

    def clean(self):
        if self.check_in >= self.check_out:
            raise models.ValidationError("Check-out must be after check-in")

class Review(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.property.title} by {self.guest.username}"