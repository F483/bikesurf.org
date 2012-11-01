from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):

    user        = models.ForeignKey(User)
    street      = models.CharField(max_length=1024)
    city        = models.CharField(max_length=1024)
    postalcode  = models.CharField(max_length=1024)
    country     = models.CharField(max_length=1024)
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.street, self.city, self.postalcode, self.country)
        return u"id: %s; user_id: %s; street: %s; city: %s; postalcode: %s; country: %s" % args
