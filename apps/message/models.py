# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models


class Message(models.Model):

    sender       = models.ForeignKey('account.Account', related_name='messages_sent') # None => system
    recipient    = models.ForeignKey('account.Account', related_name='messages_received')
    content      = models.TextField()
   
    # related
    message      = models.ForeignKey('self', related_name='replies', null=True, blank=True)
    bike         = models.ForeignKey('bike.Bike', null=True, blank=True)
    borrow       = models.ForeignKey('borrow.Borrow', null=True, blank=True)
    join_request = models.ForeignKey('team.JoinRequest', null=True, blank=True)
    join_request = models.ForeignKey('team.RemoveRequest', null=True, blank=True)

    # meta
    created_on   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        args = (self.id, self.sender.id, self.recipient.id)
        return u"id: %s; sender_id: %s; recipient_id: %s" % args


