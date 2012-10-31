from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):

    street      = models.CharField(max_length=1024) # only visible if user is borrowing a bike
    city        = models.CharField(max_length=1024)
    postalcode  = models.CharField(max_length=1024)
    country     = models.CharField(max_length=1024)
    
    # meta
    created_on  = models.DateTimeField()
    updated_on  = models.DateTimeField()


