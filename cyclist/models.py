from django.db import models
from django.contrib.auth.models import User
from address.models import Address


ROLES = ['owner', 'manager', 'mechanic'] # TODO define roles and group workflow
ROLE_CHOICES = [(role, role) for role in ROLES]


class Cyclist(models.Model):

    user        = models.ForeignKey(User)
    description = models.TextField()
    is_group    = models.BooleanField(default=False)
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.is_group)
        return u"id: %s; user_id: %s; is_group: %s" % args


class CyclistMember(models.Model):

    member      = models.ForeignKey(Cyclist, related_name='groups')
    group       = models.ForeignKey(Cyclist, related_name='members')
    role        = models.CharField(max_length=256, choices=ROLE_CHOICES)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.member.id, self.group, self.role)
        return u"id: %s; memeber_id: %s; group_id: %s; role: %s" % args


