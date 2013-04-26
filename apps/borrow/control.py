# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from apps.team import control as team_control
from apps.borrow.models import Borrow
from apps.borrow.models import Rating
from apps.borrow.models import Log
from apps.team import control as team_control


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
    is_member_state = borrow.state in member_states
    if is_member_state and team_control.is_member(account, borrow.bike.team):
        return True
    is_borrow_state = borrow.state in borrower_states
    if (is_borrow_state and account == borrow.borrower):
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
    if not team_control.is_member(account, borrow.bike.team):
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


