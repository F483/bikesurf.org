from django.db import models
from django.contrib.auth.models import User
from station.models import Station


KINDS = [
    'normal', # comfort, hybrid, trekking, citybike
    'bmx', 
    'cargobike',
    'cruiser',
    'electric', 
    'fixie', 
    'folding', 
    'kids',
    'mountainbike', 
    'recumbent',
    'roadbike', 
    'tandem',
    'unicycle'
]
KIND_CHOICES = [(kind, kind) for kind in KINDS]


GENDER = ['neutral', 'female', 'male']
GENDER_CHOICES = [(gender, gender) for gender in GENDER]


class Bike(models.Model):

    owner       = models.ForeignKey(User)
    name        = models.CharField(max_length=1024)
    description = models.TextField()
    available   = models.BooleanField(default=True)
    location    = models.ForeignKey(Station) # must belong to owner
    lockcode    = models.CharField(max_length=1024)
    
    # Usefull properties to filter by.
    kind        = models.CharField(max_length=256, choices=KIND_CHOICES, default='normal')
    gender      = models.CharField(max_length=256, choices=GENDER_CHOICES, default='neutral')
    lights      = models.BooleanField(default=False) # to cycle when dark
    fenders     = models.BooleanField(default=False) # to cycle when wet
    rack        = models.BooleanField(default=False) # to carry stuff
    basket      = models.BooleanField(default=False) # to put stuff in
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.owner.id, self.name)
        return u"id: %s; owner_id: %s; name: %s" % args


class BikePicture(models.Model):

    bike        = models.ForeignKey(Bike)
    image       = models.ImageField(upload_to='db/bike_images') # FIXME use hash as name to avoid collisisons
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.bike.id)
        return u"id: %s; bike_id: %s" % args

