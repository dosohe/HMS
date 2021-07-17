from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    slug = models.SlugField(db_index=True, unique=True, max_length=100) 
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    flat = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    net_income = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.slug}'

