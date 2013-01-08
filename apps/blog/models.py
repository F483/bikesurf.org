# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateTimeField


class Blog(Model):

    team = ForeignKey("team.Team", related_name="blogs")
    name = CharField(max_length=1024)
    content = TextField() # TODO make wiki or markdown

    # meta
    created_by = ForeignKey("account.Account", related_name="blogs_created")
    created_on = DateTimeField(auto_now_add=True)
    updated_by = ForeignKey("account.Account", related_name="blogs_updated")
    updated_on = DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:
              
        unique_together = (("team", "name")) 
        ordering = ["-created_on"]


