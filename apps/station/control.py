# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.core.exceptions import PermissionDenied
from apps.station.models import Station
from apps.borrow.models import Borrow


def can_delete(account, station):
    today = datetime.datetime.now().date()
    return not (
        # account must be a member of the stations team
        account not in station.team.members.all() or 

        # no bike can be currently at the station
        len(station.bikes.all()) or 

        # no bike can be heading to the station in the future
        len(Borrow.objects.filter(active=True, dest=station, finish__gte=today))
    )


def create( account, team, responsable, 
            active, street, city, postalcode, country ):
    station = Station()
    station.created_by = account
    station.updated_by = account
    station.team = team
    station.responsable = responsable
    station.active = active
    station.street = street
    station.city = city
    station.postalcode = postalcode
    station.country = country
    station.save()
    return station


def edit( account, station, responsable, 
          active, street, city, postalcode, country ):
    if not active and not can_delete(account, station):
        raise PermissionDenied
    station.updated_by = account
    station.responsable = responsable
    station.active = active
    station.street = street
    station.city = city
    station.postalcode = postalcode
    station.country = country
    station.save()
    return station


def delete(account, station):
    if not can_delete(account, station):
        raise PermissionDenied
    station.delete()

