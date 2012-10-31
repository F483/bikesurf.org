from django.db import models
from django.contrib.auth.models import User


class Bike(models.Model):

    owner       = models.ForeignKey(User)
    name        = models.CharField(max_length=1024)
    description = models.TextField()
    available   = models.BooleanField()
    
    # Usefull properties to filter by.
    kind        = models.CharField(max_length=256)   # 'mountainbike', 'roadbike', 'fixie', etc ...
    lights      = models.BooleanField(default=False) # to cycle when dark
    fenders     = models.BooleanField(default=False) # to cycle when wet
    rack        = models.BooleanField(default=False) # to carry stuff
    basket      = models.BooleanField(default=False) # to put stuff in
    
    # meta
    created_on  = models.DateTimeField()
    updated_on  = models.DateTimeField()
