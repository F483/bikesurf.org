# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.core.exceptions import PermissionDenied
from apps.bike.models import Bike
from apps.team import control as team_control
from apps.borrow import control as borrow_control
from apps.team.utils import assert_member
from apps.gallery.control import create as create_gallery
from apps.gallery.control import delete as delete_gallery


def available(team, start, finish, include_reserve=False, include_bike=None):
    """ List bikes available for a team in a given date range. 
    Optionally include reserve bikes and one additional bike.
    """
    borrows = team.borrows.filter(state="ACCEPTED")
    borrows = borrows.exclude(start__gt=finish).exclude(finish__lt=start)
    bikes = team.bikes.filter(active=True)
    if not include_reserve:
        bikes = bikes.filter(reserve=False)
    bikes = bikes.exclude(borrows__in=borrows)
    if include_bike:
        bikes = bikes | Bike.objects.filter(id=include_bike.id)
    return bikes


def has_future_borrows(bike):
    """ Checks if bike is borrowed in the future. """
    today = datetime.datetime.now().date()
    return bool(len(bike.borrows.filter(active=True, finish__gte=today)))


def currently_borrowed(bike):
    """ Checks if bike is currently borrowed. """
    today = datetime.datetime.now().date()
    qs = bike.borrows.filter(active=True)
    qs = qs.exclude(finish__lt=today)
    qs = qs.exclude(start__gt=today)
    return bool(len(qs))


def can_change_station(account, bike, station):
    """ Check if an account can change the bike station.
    Account must be a team member, bike not currently borrowed and
    station must be active.
    """
    return (station and station.active and bike.team == station.team and 
            team_control.is_member(account, bike.team) and 
            not currently_borrowed(bike))


def can_deactivate(account, bike):
    """ Check if an account can deactivate a bike.
    Account must be a team member and bike not borrowed in the future.
    """
    return (team_control.is_member(account, bike.team) and 
            not has_future_borrows(bike))


def can_delete(account, bike):
    """ Check if an account can delete a bike.
    Account must be a team member and bike not borrowed in the future.
    """
    return (team_control.is_member(account, bike.team) 
            and not has_future_borrows(bike))


def create( account, team, name, image, description, active, reserve, station, 
            lockcode, size, lights ):
    assert_member(account, team)
    bike = Bike()
    bike.team = team
    bike.name = name
    bike.gallery = create_gallery(account, image, team)
    bike.description = description
    bike.active = active
    bike.reserve = reserve
    bike.station = station
    bike.lockcode = lockcode
    bike.size = size
    bike.lights = lights
    bike.created_by = account
    bike.updated_by = account
    bike.save()
    return bike


def edit_is_allowed(account, bike, name, description, active, reserve, station, 
                    lockcode, size, lights):
    if not team_control.is_member(account, bike.team):
        return False
    if bike.active and not active and not can_deactivate(account, bike):
        return False
    if bike.station != station and not station.active:
        return False
    if bike.station != station and not can_change_station(account, bike, station):
        return False
    return True

def _change_station(account, bike, station):
    today = datetime.datetime.now().date()
    prev_borrow = borrow_control.get_prev_borrow(bike, today)
    if prev_borrow:
        prev_borrow.dest = station
        prev_borrow.save()
        borrow_control.log(account, prev_borrow, 
                           "Changed Drop-Off station.", "EDIT")
    yesterday = today + datetime.timedelta(days=-1)
    next_borrow = borrow_control.get_next_borrow(bike, yesterday)
    if next_borrow:
        next_borrow.src = station
        next_borrow.save()
        borrow_control.log(account, next_borrow, 
                           "Changed Pick-Up station", "EDIT")


def edit( account, bike, name, description, active, reserve, station, lockcode, 
          size, lights ):
    if not edit_is_allowed(account, bike, name, description, active, reserve, 
                           station, lockcode, size, lights):
        raise PermissionDenied
    if bike.station != station:
        _change_station(account, bike, station)
    bike.name = name
    bike.description = description
    bike.active = active
    bike.reserve = reserve
    bike.station = station
    bike.lockcode = lockcode
    bike.size = size
    bike.lights = lights
    bike.updated_by = account
    bike.save()
    return bike


def delete(account, bike):
    if not can_delete(account, bike):
        raise PermissionDenied
    for borrow in bike.borrows.all():
        borrow.bike = None
        borrow.save()
    delete_gallery(account, bike.gallery)
    bike.delete()


def update_stations():
    today = datetime.datetime.now().date()
    bikes = Bike.objects.filter(active=True)
    for bike in bikes:
        last_borrow = borrow_control.get_prev_borrow(bike, today)
        if last_borrow and last_borrow.dest != bike.station:
            bike.station = last_borrow.dest
            bike.save()


