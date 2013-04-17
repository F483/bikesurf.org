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
    borrower_states = ["REQUEST", "MEETUP", "ACCEPTED"] 
    member_states = ["MEETUP", "ACCEPTED"]
    members = borrow.bike.team.members.all()
    if (borrow.state in member_states and account in members):
        return True
    if (borrow.state in borrower_states and account == borrow.borrower):
        return True
    return False


def _finish(borrow):
    is_running = borrow.state == "MEETUP" or borrow.state == "ACCEPTED"
    if not is_running or len(Rating.objects.filter(borrow=borrow)) != 2:
        return
    borrow.state = "FINISHED"
    borrow.save()
    _log(None, borrow, "", "FINISHED")
    return borrow


def can_rate_team(account, borrow):
    today = datetime.datetime.now().date()
    if not today >= borrow.start:
        return False # to soon
    if not borrow.state == 'MEETUP' and not borrow.state == 'ACCEPTED':
        return False # wrong state
    if not account in borrow.bike.team.members.all():
        return False # only members
    if len(Rating.objects.filter(borrow=borrow, originator='LENDER')):
        return False # already rated but not by borrower
    return True


def can_rate_my(account, borrow):
    today = datetime.datetime.now().date()
    if not today >= borrow.start:
        return False # to soon
    if not borrow.state == 'MEETUP' and not borrow.state == 'ACCEPTED':
        return False # wrong state
    if account != borrow.borrower:
        return False # only borrower
    if len(Rating.objects.filter(borrow=borrow, originator='BORROWER')):
        return False # already rated but not by team
    return True


def rate_team(account, borrow, rating_value, note):
    rating = Rating()   
    rating.borrow = borrow
    rating.rating = rating_value
    rating.account = account
    rating.originator = "LENDER"
    rating.save()
    log = _log(account, borrow, note, "RATE_TEAM")
    return _finish(borrow)


def rate_my(account, borrow, rating_value, note):
    rating = Rating()   
    rating.borrow = borrow
    rating.rating = rating_value
    rating.account = account
    rating.originator = "BORROWER"
    rating.save()
    log = _log(account, borrow, note, "RATE_MY")
    return _finish(borrow)


def create(bike, account, start, finish, note):
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


def respond(account, borrow, state, note):
    borrow.state = state
    borrow.active = state != "REJECTED"
    borrow.save()
    log = _log(account, borrow, note, "RESPOND")
    return borrow


def cancel(account, borrow, note):
    borrow.state = "CANCELED"
    borrow.active = False
    borrow.save()
    log = _log(account, borrow, note, "CANCLE")
    return borrow


