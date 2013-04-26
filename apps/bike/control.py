# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.core.exceptions import PermissionDenied
from apps.bike.models import Bike
from apps.team import control as team_control
from apps.team.utils import assert_member
from apps.gallery.control import create as create_gallery
from apps.gallery.control import delete as delete_gallery


def in_use(bike):
    """ Checks if bike is borrowed in the future. """
    today = datetime.datetime.now().date()
    return len(bike.borrows.filter(active=True, finish__gte=today))


def can_deactivate(account, bike):
    """ Check if an account can deactivate a bike.
    Account must be a team member and bike not borrowed in the future.
    """
    return team_control.is_member(account, bike.team) and not in_use(bike)


def can_delete(account, bike):
    """ Check if an account can delete a bike.
    Account must be a team member and bike not borrowed in the future.
    """
    return team_control.is_member(account, bike.team) and not in_use(bike)


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


def edit( account, bike, name, description, active, reserve, station, lockcode, 
          size, lights ):
    assert_member(account, bike.team)
    if bike.active and not active and not can_deactivate(account, bike):
        raise PermissionDenied
    if bike.station != station and not station.active:
        raise PermissionDenied
    if bike.station != station:
        pass # TODO change src station of next borrow and what to do with inactive borrows?
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
    assert_member(account, bike.team)
    if not can_delete(account, bike):
        raise PermissionDenied
    for borrow in bike.borrows.all():
        borrow.bike = None
        borrow.save()
    delete_gallery(account, bike.gallery)
    bike.delete()


