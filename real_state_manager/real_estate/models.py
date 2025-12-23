from django.db import models

from real_state_manager.guests.models import Guest
from real_state_manager.locations.models import Location
from real_state_manager.users.models import User


# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    availability = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location} - Max: {self.max_guests}"


class Reservation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    renting_price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_guests = models.IntegerField()
    description = models.TextField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.property} - {self.guest.name} - {self.check_in} - {self.check_out}"
        )
