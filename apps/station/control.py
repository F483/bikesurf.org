# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.core.exceptions import PermissionDenied
from apps.station.models import Station
from apps.borrow.models import Borrow
from apps.team import control as team_control


def can_edit(account, station):
    # account must be a member of the stations team
    return team_control.is_member(account, station.team)


def in_use(station):
    today = datetime.datetime.now().date()
    return (
        # bikes currently at the station
        len(station.bikes.all()) or 
        # bikes heading to the station in the future
        len(Borrow.objects.filter(active=True, dest=station, finish__gte=today))
    )


def can_delete(account, station):
    return can_edit(account, station) and not in_use(station)


def can_deactivate(account, station):
    return can_edit(account, station) and not in_use(station)


def create( account, team, responsable, 
            active, street, city, postalcode ):
    station = Station()
    station.created_by = account
    station.updated_by = account
    station.team = team
    station.responsable = responsable
    station.active = active
    station.street = street
    station.city = city
    station.postalcode = postalcode
    station.save()
    return station


def edit( account, station, responsable, 
          active, street, city, postalcode ):
    if not active and not can_deactivate(account, station):
        raise PermissionDenied
    station.updated_by = account
    station.responsable = responsable
    station.active = active
    station.street = street
    station.city = city
    station.postalcode = postalcode
    station.save()
    return station


def delete(account, station):
    if not can_delete(account, station):
        raise PermissionDenied
    station.delete()

