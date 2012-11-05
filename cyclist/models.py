from django.db import models
from django.contrib.auth.models import User


ROLES = [
    'owner',      # can update team data and add remove users/roles
    'manager',    # can lend team bikes to/from team stations
]
ROLE_CHOICES = [(role, role) for role in ROLES]


class Cyclist(models.Model):

    user         = models.ForeignKey(User)
    is_team      = models.BooleanField(default=False)
    description  = models.TextField()
    couchsurfing = models.URLField()
    facebook     = models.URLField()
    twitter      = models.URLField()
    googleplus   = models.URLField()
    blog         = models.URLField()
    mobile       = models.CharField(max_length=1024)
    skype        = models.CharField(max_length=1024)
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.is_team)
        return u"id: %s; user_id: %s; is_team: %s" % args


class CyclistMember(models.Model):

    member      = models.ForeignKey(Cyclist, related_name='teams')
    team        = models.ForeignKey(Cyclist, related_name='members')
    role        = models.CharField(max_length=256, choices=ROLE_CHOICES)

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.member.id, self.team, self.role)
        return u"id: %s; memeber_id: %s; team_id: %s; role: %s" % args


class CyclistPicture(models.Model):

    cyclist     = models.ForeignKey(Cyclist)
    image       = models.ImageField(upload_to='db/cyclist_images') # FIXME use hash as name to avoid collisisons
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.cyclist.id)
        return u"id: %s; cyclist_id: %s" % args


