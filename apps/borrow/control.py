# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from apps.borrow.models import Borrow
from apps.borrow.models import Log


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


def _log(account, borrow, note):
    log = Log()
    log.borrow = borrow
    log.initiator = account
    log.state = borrow.state
    log.note = note
    log.save()
    return log


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
    log = _log(account, borrow, note)
    return borrow, log


def respond(account, borrow, state, note):
    borrow.state = state
    borrow.active = state != "REJECTED"
    borrow.save()
    log = _log(account, borrow, note)
    return borrow, log


def cancel(account, borrow, note):
    borrow.state = "CANCELED"
    borrow.active = False
    borrow.save()
    log = _log(account, borrow, note)
    return borrow, log


