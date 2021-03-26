from django.db import models
from statistics import mean


class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    rating = models.JSONField(blank=True, null=True)

    @property
    def avg_rating(self):
        if self.rating:
            return mean(self.rating)
        return

    @property
    def rates_number(self):
        if self.rating:
            return len(self.rating)
        return 0

    def __str__(self):
        return f"<Make: {self.make}, Model: {self.model}>"

