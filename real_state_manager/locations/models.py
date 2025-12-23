from django.db import models
from map_location.fields import LocationField


# Create your models here.
class Location(models.Model):
    cep = models.CharField(max_length=8)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=100, null=True, blank=True)  # noqa: DJ001
    country = models.CharField(max_length=100, default="Brazil")
    location = LocationField(
        "Pos",
        blank=True,
        null=True,
        options={
            "map": {
                "center": [-23.55, -46.63],
                "zoom": 12,
            },
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street} - {self.city} - {self.state} -  {self.country}"
