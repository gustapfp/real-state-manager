from django.db import models

from real_state_manager.locations.models import Location


# Create your models here.
class Guest(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.cpf} - {self.email} - {self.phone}"
