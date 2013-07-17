# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateTimeField
from sanitizer.models import SanitizedCharField
from config.settings import SANITIZER_ALLOWED_TAGS, SANITIZER_ALLOWED_ATTRIBUTES


class Blog(Model):

    team       = ForeignKey("team.Team", related_name="blogs")
    name       = CharField(max_length=1024)
    content    = SanitizedCharField(
                   max_length=50000, allowed_tags=SANITIZER_ALLOWED_TAGS, 
                   allowed_attributes=SANITIZER_ALLOWED_ATTRIBUTES, strip=False
               )

    # meta
    created_by = ForeignKey("account.Account", related_name="blogs_created")
    created_on = DateTimeField(auto_now_add=True)
    updated_by = ForeignKey("account.Account", related_name="blogs_updated")
    updated_on = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:
              
        unique_together = (("team", "name")) 
        ordering = ["-created_on"]


