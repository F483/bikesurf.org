# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django_countries import countries
from django.shortcuts import _get_queryset

from apps.borrow.models import Borrow
from apps.bike.models import Bike
from apps.station.models import Station


COUNTRIES = [('', '---------')] + list(countries.COUNTRIES)


def uslugify(ustr):
    """ because slugify is shit with unicode """
    return slugify(unidecode(ustr))


def render_response(request, template, args):
    from apps.borrow import control as borrow_control # circular import ...
    args.update({ 
        "current_user" : request.user,
        "current_path" : request.path,
    })
    if request.user.is_authenticated():
        account = request.user.accounts.all()[0]
        borrows = Borrow.objects.filter(borrower=account)
        borrows = borrows.exclude(state="CANCELED").exclude(state="FINISHED")
        args.update({ 
            "current_account" : account,
            "borrow_count" : len(borrows),
            "current_account_teams" : account.teams.all(),
            "station_count" : len(Station.objects.filter(responsable=account)),
            "outgoing_count" : len(borrow_control.outgoing_list(account)),
            "incoming_count" : len(borrow_control.incoming_list(account)),
        })
    args.update(csrf(request))
    # TODO check for mobile browser and use mobile template if it exists
    return render_to_response(template, args)


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

