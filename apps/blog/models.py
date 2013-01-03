# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _


class Blog(models.Model):

    team        = models.ForeignKey("team.Team", related_name="blogs")
    name        = models.CharField(max_length=1024)
    content     = models.TextField() # TODO make wiki or markdown

    # meta
    created_by  = models.ForeignKey("account.Account", related_name="blogs_created")
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey("account.Account", related_name="blogs_updated")
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:
              
        unique_together = (("team", "name")) 
        ordering = ["-created_on"]


