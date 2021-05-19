from django.db import models
from django.contrib.auth.models import User, auth
from django.db.models.base import Model

# Create your models here.

class Advisor(models.Model):
    name = models.CharField(max_length=50)
    photo_url = models.URLField(max_length=1000)

class Booking(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    advisorid = models.ForeignKey(Advisor,on_delete=models.CASCADE)
    booking_time = models.DateTimeField()