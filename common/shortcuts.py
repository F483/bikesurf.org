# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.core.validators import RegexValidator
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


# A human readable Id for urls TODO make custom Field class
URL_NAME = "[\w.@+-]{1,30}" # Same format as 'auth.User.username'
MODEL_NAME = models.CharField(max_length=30, unique=True, validators=[RegexValidator('^%s$' % URL_NAME)])


def render_response(request, template, args):
    # accountbar data
    args.update({
        'current_user' : request.user,
        'message_count' : 0, # TODO get count
        'borrow_count' : 0, # TODO get count
    })
    args.update(csrf(request))
    return render_to_response(template, args)

