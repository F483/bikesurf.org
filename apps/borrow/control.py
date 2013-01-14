# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from apps.borrow.models import Borrow
from apps.borrow.models import Rating
from apps.borrow.models import Log


def _log(account, borrow, note, action):
    log = Log()
    log.borrow = borrow
    log.initiator = account
    log.action = action
    log.note = note
    log.save()
    return log


def can_cancel(account, borrow):
    today = datetime.datetime.now().date()
    if borrow.start <= today:
        return False
    if (borrow.state in ["REQUEST", "MEETUP", "ACCEPTED"] 
            and account == borrow.borrower):
        return True
    if (borrow.state in ["MEETUP", "ACCEPTED"] 
            and account in borrow.bike.team.members.all()):
        return True
    return False


def can_rate_team(account, borrow):
    today = datetime.datetime.now().date()
    if not today > borrow.start:
        return False # to soon
    if not borrow.state == 'MEETUP' and not borrow.state == 'ACCEPTED':
        return False # wrong state
    if not account in borrow.bike.team.members.all():
        return False # only members
    if len(Rating.objects.filter(borrow=borrow, originator='LENDER')):
        return False # already rated but not finished
    return True


def can_rate_my(account, borrow):
    today = datetime.datetime.now().date()
    if not today > borrow.start:
        return False # to soon
    if not borrow.state == 'MEETUP' and not borrow.state == 'ACCEPTED':
        return False # wrong state
    if account != borrow.borrower:
        return False # only borrower
    if len(Rating.objects.filter(borrow=borrow, originator='BORROWER')):
        return False # already rated but not finished
    return True


def rate_team(account, borrow, rating_value, note):
    rating = Rating()   
    rating.borrow = borrow
    rating.rating = rating_value
    rating.account = account
    rating.originator = "LENDER"
    rating.save()
    log = _log(account, borrow, note, "RATE_TEAM")
    return rating, log


def rate_my(account, borrow, rating, note):
    # TODO
    pass


def create(bike, account, start, finish, note):
    borrow = Borrow()
    borrow.bike = bike
    borrow.borrower = account
    borrow.start = start
    borrow.finish = finish
    borrow.active = False
    borrow.state = "REQUEST"
    borrow.src = bike.station
    borrow.dest = bike.station
    borrow.save()
    log = _log(account, borrow, note, "CREATE")
    return borrow, log


def respond(account, borrow, state, note):
    borrow.state = state
    borrow.active = state != "REJECTED"
    borrow.save()
    log = _log(account, borrow, note, "RESPOND")
    return borrow, log


def cancel(account, borrow, note):
    borrow.state = "CANCELED"
    borrow.active = False
    borrow.save()
    log = _log(account, borrow, note, "CANCLE")
    return borrow, log


