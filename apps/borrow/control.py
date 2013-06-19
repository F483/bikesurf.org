# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.core.exceptions import PermissionDenied

from apps.borrow.models import Borrow
from apps.borrow.models import Rating
from apps.borrow.models import Log
from apps.team import control as team_control


def incoming_list(account):
    today = datetime.datetime.now().date()
    return Borrow.objects.filter(active=True, finish__gte=today, 
                                 dest__responsable=account)


def outgoing_list(account):
    today = datetime.datetime.now().date()
    return Borrow.objects.filter(active=True, start__gte=today, 
                                 src__responsable=account)


def _log(account, borrow, note, action):
    log = Log()
    log.borrow = borrow
    log.initiator = account
    log.action = action
    log.note = note
    log.save()
    return log


def can_borrow(bike):
    return (bike.active and not bike.reserve and 
            bike.station and bike.station.active)


def can_cancel(account, borrow):
    borrow_started = borrow.start <= datetime.datetime.now().date()
    is_lender = team_control.is_member(account, borrow.team)
    is_borrower = account == borrow.borrower
    lender_cancel_allowed = borrow.state in ["MEETUP", "ACCEPTED"]
    borrower_cancel_allowed = borrow.state in ["REQUEST", "MEETUP", "ACCEPTED"] 
    return (is_borrower and borrower_cancel_allowed or 
            is_lender and lender_cancel_allowed and not borrow_started)


def lender_can_rate(account, borrow):
    today = datetime.datetime.now().date()
    if not today > borrow.finish:
        return False # to soon
    if borrow.state not in ["MEETUP", "ACCEPTED"]:
        return False # wrong state
    if not team_control.is_member(account, borrow.team):
        return False # only members
    if len(Rating.objects.filter(borrow=borrow, originator='LENDER')):
        return False # already rated
    return True


def borrower_can_rate(account, borrow):
    today = datetime.datetime.now().date()
    if not today >= borrow.start:
        return False # to soon
    if borrow.state not in ["MEETUP", "ACCEPTED"]:
        return False # wrong state
    if account != borrow.borrower:
        return False # only borrower
    if len(Rating.objects.filter(borrow=borrow, originator='BORROWER')):
        return False # already rated
    return True


def lender_rate(account, borrow, rating_value, note):
    if not lender_can_rate(account, borrow):
        raise PermissionDenied
    rating = Rating()   
    rating.borrow = borrow
    rating.rating = rating_value
    rating.account = account
    rating.originator = "LENDER"
    rating.save()
    log = _log(account, borrow, note, "LENDER_RATE")
    return _finish(borrow)


def borrower_rate(account, borrow, rating_value, note):
    if not borrower_can_rate(account, borrow):
        raise PermissionDenied
    rating = Rating()   
    rating.borrow = borrow
    rating.rating = rating_value
    rating.account = account
    rating.originator = "BORROWER"
    rating.save()
    log = _log(account, borrow, note, "BORROWER_RATE")
    return _finish(borrow)


def _finish(borrow):
    if len(Rating.objects.filter(borrow=borrow)) != 2:
        return borrow # only finish when borrower and lender have rated
    borrow.state = "FINISHED"
    borrow.save()
    _log(None, borrow, "", "FINISHED")
    return borrow


def active_borrows_in_timeframe(bike, start, finish):
    """ Returns borrows in the given timeframe. finish is inclusive! """
    # other borrows starting in timeframe
    starting = list(Borrow.objects.filter(bike=bike, active=True, 
                                          start__gte=start, start__lte=finish))
    # other borrows finishing in timeframe
    ending = list(Borrow.objects.filter(bike=bike, active=True,
                                        finish__gte=start, finish__lte=finish))
    return starting + ending


def can_respond(account, borrow):
    if borrow.state != "REQUEST":
        return False # borrow must be in request state
    if not team_control.is_member(account, borrow.team):
        return False # not a member
    return True


def response_is_allowed(account, borrow, state):
    if not can_respond(account, borrow):
        return False
    if state == "REJECTED":
        return True
    today = datetime.datetime.now().date()
    if borrow.finish <= today:
        return False # to late
    if not can_borrow(borrow.bike):
        return False
    if active_borrows_in_timeframe(borrow.bike, borrow.start, borrow.finish):
        return False
    return True


def respond(account, borrow, state, note):
    if not response_is_allowed(account, borrow, state):
        raise PermissionDenied
    borrow.state = state
    borrow.active = state != "REJECTED"
    borrow.save()
    log = _log(account, borrow, note, "RESPOND")
    return borrow


def cancel(account, borrow, note):
    if not can_cancel(account, borrow):
        raise PermissionDenied
    borrow.state = "CANCELED"
    borrow.active = False
    borrow.save()
    log = _log(account, borrow, note, "CANCLE")
    return borrow


def creation_is_allowed(account, bike, start, finish):
    if not can_borrow(bike):
        return False
    # check timeframe
    today = datetime.datetime.now().date()
    if start <= today:
        return False
    if finish < start:
        return False
    if len(active_borrows_in_timeframe(bike, start, finish)):
        return False
    return True


def create(account, bike, start, finish, note):
    if not creation_is_allowed(account, bike, start, finish):
        raise PermissionDenied
    borrow = Borrow()
    borrow.bike = bike
    borrow.team = bike.team
    borrow.borrower = account
    borrow.start = start
    borrow.finish = finish
    borrow.active = False
    borrow.state = "REQUEST"
    borrow.src = bike.station
    borrow.dest = bike.station
    borrow.save()
    log = _log(account, borrow, note, "CREATE")
    return borrow


