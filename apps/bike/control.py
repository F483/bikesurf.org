# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.exceptions import PermissionDenied
from apps.bike.models import Bike
from apps.team.utils import assert_member
from apps.gallery.control import create as create_gallery
from apps.gallery.control import delete as delete_gallery


def can_delete(account, bike):
    is_member = account in bike.team.members.all()
    active_borrows = len(bike.borrows.filter(active=True))
    return is_member and not active_borrows


def create( account, team, name, image, description, active, reserve, station, 
            lockcode, size, lights ):
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


