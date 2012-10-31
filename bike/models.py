from django.db import models
from django.contrib.auth.models import User
from address.models import Address


class Bike(models.Model):

    owner       = models.ForeignKey(User)
    name        = models.CharField(max_length=1024)
    description = models.TextField()
    available   = models.BooleanField()
    address     = models.ForeignKey(Address)
    
    # Usefull properties to filter by.
    kind        = models.CharField(max_length=256)   # 'mountainbike', 'roadbike', 'fixie', etc ...
    lights      = models.BooleanField(default=False) # to cycle when dark
    fenders     = models.BooleanField(default=False) # to cycle when wet
    rack        = models.BooleanField(default=False) # to carry stuff
    basket      = models.BooleanField(default=False) # to put stuff in
    
    # meta
    created_on  = models.DateTimeField()
    updated_on  = models.DateTimeField()


class BikePicture(models.Model):

    bike        = models.ForeignKey(Bike)
    image       = models.ImageField(upload_to='db/bike_images')
    
    # meta
    created_on  = models.DateTimeField()
    updated_on  = models.DateTimeField()


