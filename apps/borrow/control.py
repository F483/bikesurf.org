# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from apps.common.shortcuts import send_mail
from apps.borrow.models import Borrow
from apps.borrow.models import Rating
from apps.borrow.models import Log
from apps.borrow import signals
from apps.team import control as team_control
from apps.account import control as account_control
from config.settings import BORROW_MIN_BOOK_IN_ADVANCE_DAYS as MIN_BOOK


def log(account, borrow, note, action):
    if not account: # get site account if available
        account = account_control.get_site_account()
    l = Log()
    l.borrow = borrow
    l.initiator = account
    l.action = action
    l.note = note
    l.save()
    signals.borrow_log_created.send(sender=log, log=l)
    return l


################
# BORROW CHAIN #
################

def _remove_from_borrow_chain(account, borrow):
    """ Pass the borrow being removed from the chain.
        Ensure that borrow chain src and dest stations always match. 

        Before                      After
          x>1 - 1>B>2 - 2>x           x>1 -   -   - 1>x
        1>b>2 - 2>B>3 - 3>x         1>b>2 -   -   - 2>x
          x>1 - 1>B>2 - 2>b>3         x>1 -   -   - 1>b>3
        1>b>2 - 2>B>3 - 3>b>4       1>b>2 -   -   - 2>b>4
    """
    if borrow.state != "ACCEPTED":
        raise Exception("Only accepted borrows allowed!")
    next_borrow = get_next_borrow(borrow.bike, borrow.finish)
    if next_borrow and next_borrow.src != borrow.src:
         next_borrow.src = borrow.src
         next_borrow.save()
         log(account, next_borrow, "Changed Pick-Up station.", "EDIT")


def _insert_into_borrow_chain(borrow, bike):
    """ Pass the borrow being inserted into the chain.
        Ensure that borrow chain src and dest stations always match. 

         jul     aug     sep         jul     aug     sep
        Before                      After
          x>1 -   -   - 1>x           x>1 - 1>B>1 - 1>x                         
        1>b>2 -   -   - 2>x         1>b>2 - 2>B>2 - 2>x                         
          x>1 -   -   - 1>b>3         x>1 - 1>B>1 - 1>b>3                       
        1>b>2 -   -   - 2>b>4       1>b>2 - 2>B>2 - 2>b>4 
    """
    if borrow.state != "ACCEPTED":
        raise Exception("Only accepted borrows allowed!")
    prev_borrow = get_prev_borrow(bike, borrow.start)
    borrow.src = prev_borrow and prev_borrow.dest or bike.station
    borrow.dest = borrow.src
    borrow.bike = bike


###########
# COMMENT #
###########


def can_comment(account, borrow):
    if account == borrow.borrower:
        return True
    if team_control.is_member(account, borrow.team):
        return True
    return False


def comment(account, borrow, note):
    if not can_comment(account, borrow):
        raise PermissionDenied
    log(account, borrow, note, "COMMENT")


##########
# QUERRY #
##########


def get_next_borrow(bike, finish):
    if not bike:
        return None
    qs = Borrow.objects.filter(active=True, bike=bike, start__gt=finish)
    borrows = list(qs.order_by("start")[:1]) # order and limit
    return borrows and borrows[0] or None                  


def get_prev_borrow(bike, start):
    if not bike:
        return None
    qs = Borrow.objects.filter(active=True, bike=bike, finish__lt=start)
    borrows = list(qs.order_by("-finish")[:1]) # order and limit
    return borrows and borrows[0] or None                  


def active_borrows_in_timeframe(bike, start, finish, exclude=None):
    """ Returns borrows in the given timeframe. finish is inclusive! """
    if not bike:
        raise Exception("BIKE REQUIRED!")
    qs = Borrow.objects.filter(bike=bike, active=True)
    qs = qs.exclude(start__gt=finish)
    qs = qs.exclude(finish__lt=start)
    if exclude:
        qs = qs.exclude(id=exclude.id)
    return list(qs)


def to_list_data(borrows, team_link=False, columns="ALL"):
    def borrow2entrie(borrow):
        base_url = team_link and ("/%s" % borrow.team.link) or ""
        src = borrow.src and borrow.src.street or None
        dest = borrow.dest and borrow.dest.street or None
        bike_name = borrow.bike and borrow.bike.name or _("DELETED")
        if columns == "ARRIVALS":
            return {
                "labels" : [ borrow.borrower, bike_name, borrow.finish, dest ], 
                "url" : "%s/borrow/view/%s" % (base_url, borrow.id)
            }
        elif columns == "DEPARTURES":
            return {
                "labels" : [ borrow.borrower, bike_name, borrow.start, src ], 
                "url" : "%s/borrow/view/%s" % (base_url, borrow.id)
            }
        else:
            return {
                "labels" : [ 
                    borrow.borrower, bike_name, borrow.start, borrow.finish, 
                    src, dest, borrow.state
                ], 
                "url" : "%s/borrow/view/%s" % (base_url, borrow.id)
            }
    if columns == "ARRIVALS":
        return { 
            "columns" : [ 
                _("BORROWER"), _("BIKE"), _("DATE_TO"), _("STATION_TO") 
            ], 
            "entries" : map(borrow2entrie, borrows) 
        }
    elif columns == "DEPARTURES":
        return { 
            "columns" : [ 
                _("BORROWER"), _("BIKE"), _("DATE_FROM"), _("STATION_FROM") 
            ], 
            "entries" : map(borrow2entrie, borrows) 
        }
    else:
        return { 
            "columns" : [
                _("BORROWER"), _("BIKE"), _("DATE_FROM"), _("DATE_TO"),
                _("STATION_FROM"), _("STATION_TO"), _("BORROW_STATE"),
            ], 
            "entries" : map(borrow2entrie, borrows) 
        }


def arrivals(account):
    today = datetime.datetime.now().date()
    borrows = Borrow.objects.filter(
            active=True, finish__gte=today, dest__responsible=account
    )
    borrows = borrows.order_by("finish")
    return borrows


def departures(account):
    today = datetime.datetime.now().date()
    borrows = Borrow.objects.filter(
            active=True, start__gte=today, src__responsible=account
    )
    borrows = borrows.order_by("start")
    return borrows


##############
# RESPONDING #
##############


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


def accept_station(borrow):
    """ The station the borrow would have as src and dest if it were to be 
    accepted at this very moment.
    """
    prev_borrow = get_prev_borrow(borrow.bike, borrow.start)
    return prev_borrow and prev_borrow.dest or borrow.bike.station


def respond(account, borrow, state, note):
    if not response_is_allowed(account, borrow, state):
        raise PermissionDenied
    borrow.state = state
    borrow.active = state != "REJECTED"
    if state != "REJECTED": # set stations
        borrow.src = accept_station(borrow)
        borrow.dest = borrow.src
    borrow.save()
    log(account, borrow, note, "RESPOND")
    return borrow


#############
# CANCELING #
#############


def can_cancel(account, borrow):
    today = datetime.datetime.now().date()
    if borrow.finish < today: # borrow ended
        return False
    is_lender = team_control.is_member(account, borrow.team)
    is_borrower = account == borrow.borrower
    lender_state = borrow.state in ["ACCEPTED"]
    borrower_state = borrow.state in ["REQUEST", "ACCEPTED"] 
    return (is_borrower and borrower_state or 
            is_lender and lender_state)


def cancel(account, borrow, note):
    if not can_cancel(account, borrow):
        raise PermissionDenied
    if borrow.state == "ACCEPTED": # ensure borrow chain unbroken
        _remove_from_borrow_chain(account, borrow)
        borrow.src = None
        borrow.dest = None
    borrow.state = "CANCELED"
    borrow.active = False
    borrow.save()
    log(account, borrow, note, "CANCEL")
    return borrow


#################
# CREATE BORROW #
#################


def can_borrow(bike):
    return (bike and bike.active and not bike.reserve and 
            bike.station and bike.station.active)


def creation_is_allowed(account, bike, start, finish, exclude=None):
    if not can_borrow(bike):
        return False
    # check timeframe
    if finish < start:
        return False
    if not team_control.is_member(account, bike.team):
        today = datetime.datetime.now().date()
        minstart = today + datetime.timedelta(days=MIN_BOOK)
        if start < minstart:
            return False
    if len(active_borrows_in_timeframe(bike, start, finish, exclude=exclude)):
        return False
    return True


def create(account, bike, start, finish, note):
    if not account_control.has_required_info(account):
        raise PermissionDenied
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
    borrow.save()
    log(account, borrow, note, "CREATE")
    return borrow


##########
# RATING #
##########


def _finish(account, borrow):
    if len(Rating.objects.filter(borrow=borrow)) != 2:
        return borrow # only finish when borrower and lender have rated
    borrow.state = "FINISHED"
    borrow.save()
    log(account, borrow, "Set state to Finished.", "FINISHED")
    return borrow


def lender_can_rate(account, borrow):
    today = datetime.datetime.now().date()
    if not today > borrow.finish:
        return False # to soon
    if borrow.state not in ["ACCEPTED"]:
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
    if borrow.state not in ["ACCEPTED"]:
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
    log(account, borrow, note, "LENDER_RATE")
    return _finish(account, borrow)


def borrower_rate(account, borrow, rating_value, note):
    if not borrower_can_rate(account, borrow):
        raise PermissionDenied
    rating = Rating()   
    rating.borrow = borrow
    rating.rating = rating_value
    rating.account = account
    rating.originator = "BORROWER"
    rating.save()
    log(account, borrow, note, "BORROWER_RATE")
    return _finish(account, borrow)


###########
# EDITING #
###########


def lender_can_edit(account, borrow):
    today = datetime.datetime.now().date()
    if borrow.state not in ["REQUEST", "ACCEPTED"]:
        return False
    if borrow.finish <= today:
        return False
    if account not in borrow.team.members.all():
        return False
    return True


def lender_can_edit_dest(account, borrow):
    if not lender_can_edit(account, borrow):
        return False
    if not borrow.state == "ACCEPTED":
        return False
    return True


def borrower_can_edit(account, borrow):
    today = datetime.datetime.now().date()
    if borrow.state not in ["REQUEST", "ACCEPTED"]:
        return False
    if borrow.start <= today:
        return False
    if account != borrow.borrower:
        return False
    return True


def borrower_edit_is_allowed(account, borrow, start, finish, bike):
    if not borrower_can_edit(account, borrow):
        return False
    if not creation_is_allowed(account, bike, start, finish, exclude=borrow):
        return False
    if bike.team != borrow.team or not bike.active:
        return False
    return True


def lender_edit_is_allowed(account, borrow, start, finish, bike):
    if not lender_can_edit(account, borrow):
        return False
    if bike.team != borrow.team or not bike.active:
        return False
    if active_borrows_in_timeframe(bike, start, finish, exclude=borrow):
        return False
    return True


def lender_edit_dest_is_allowed(account, borrow, dest):
    if not lender_can_edit_dest(account, borrow):
        return False
    if dest.team != borrow.team or not dest.active:
        return False
    return True


def borrower_edit(account, borrow, start, finish, bike, note):
    if (borrow.start == start and borrow.finish == finish 
            and borrow.bike == bike):
        return # nothing changed TODO throw error here, should never get this far!
    if not borrower_edit_is_allowed(account, borrow, start, finish, bike):
        raise PermissionDenied
    if borrow.state == "ACCEPTED": # ensure borrow chain unbroken
        _remove_from_borrow_chain(account, borrow)
    borrow.start = start
    borrow.finish = finish
    borrow.bike = bike
    borrow.state = "REQUEST" # borrower edits require confirmation
    borrow.active = False
    borrow.save()
    log(account, borrow, note, "EDIT")


def lender_edit(account, borrow, start, finish, bike, note):
    if (borrow.start == start and borrow.finish == finish 
            and borrow.bike == bike):
        return # nothing changed TODO throw error here, should never get this far!
    if not lender_edit_is_allowed(account, borrow, start, finish, bike):
        raise PermissionDenied
    if borrow.state == "ACCEPTED":
        _remove_from_borrow_chain(account, borrow)
    borrow.start = start
    borrow.finish = finish
    if borrow.state == "ACCEPTED":
        _insert_into_borrow_chain(borrow, bike)
    else:
        borrow.bike = bike
    borrow.save()
    log(account, borrow, note, "EDIT")


def lender_edit_dest(account, borrow, dest, note):
    if borrow.dest == dest:
        return # nothing changed TODO throw error here, should never get this far!
    if not lender_edit_dest_is_allowed(account, borrow, dest):
        raise PermissionDenied
    next_borrow = get_next_borrow(borrow.bike, borrow.finish)
    if next_borrow:
        next_borrow.src = dest
        next_borrow.save()
        log(account, next_borrow, "Changed Pick-Up station.", "EDIT")
    borrow.dest = dest
    borrow.save()
    log(account, borrow, note, "EDIT")


##########
# EMAILS #
##########


def _borrower_emails(borrow):
    """ Get the email adresses for borrower emails.
    Mail lenders so they can answer borrower questions and see station changes.
    """
    emails = _lender_emails(borrow) 
    emails.append(account_control.get_email_or_404(borrow.borrower))
    return emails


def _lender_emails(borrow):
    if borrow.state == "ACCEPTED":
        src = borrow.src
        dest = borrow.dest
    else:
        src = accept_station(borrow)
        dest = src
    if src == dest:
        return [account_control.get_email_or_404(src.responsible)]
    else:
        src_email = account_control.get_email_or_404(src.responsible)
        dest_email = account_control.get_email_or_404(dest.responsible)
        return [src_email, dest_email]


def _get_email_templates(party, action):
    action = action.lower()
    party = party.lower()
    template = "borrow/email/{party}_{action}_{part}.txt"
    return (
        template.format(party=party, action=action, part="subject"),
        template.format(party=party, action=action, part="message"),
    )


@receiver(signals.borrow_log_created)
def log_created_borrower_callback(sender, **kwargs):
    log = kwargs["log"]
    if log.borrow.borrower == log.initiator:
        return # no need to notify user of there own actions
    today = datetime.datetime.now().date()
    if log.borrow.finish < today or log.action in ["FINISHED", "LENDER_RATE"]:
        return # no one cares, dont spam
    emails = _borrower_emails(log.borrow)
    subject, message = _get_email_templates("borrower", log.action)
    send_mail(emails, subject, message, kwargs)


@receiver(signals.borrow_log_created)
def log_created_lender_callback(sender, **kwargs):
    log = kwargs["log"]
    if log.action in ["FINISHED", "BORROWER_RATE"]:
        return # no one cares, dont spam
    sys_edit = log.initiator == None
    if sys_edit or team_control.is_member(log.initiator, log.borrow.team):
        return # not need to notify team of its own actions
    emails = _lender_emails(log.borrow)
    subject, message = _get_email_templates("lender", log.action)
    send_mail(emails, subject, message, kwargs)


def send_reminders_borrower_rate():
    today = datetime.datetime.now().date()
    borrows = Borrow.objects.filter(
        state="ACCEPTED", finish__lt=today, reminded_borrower_rate=False
    )
    for borrow in borrows:
        if len(Rating.objects.filter(borrow=borrow, originator='BORROWER')):
            continue # already rated
        emails = _borrower_emails(borrow)
        subject, message = _get_email_templates("borrower", "remind_rate")
        send_mail(emails, subject, message, { "borrow" : borrow })
        borrow.reminded_borrower_rate = True
        borrow.save()


def send_reminders_borrower_pickup():
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    borrows = Borrow.objects.filter(
        state="ACCEPTED", start=tomorrow, reminded_borrower_pickup=False
    )
    for borrow in borrows:
        emails = _borrower_emails(borrow)
        subject, message = _get_email_templates("borrower", "remind_pickup")
        send_mail(emails, subject, message, { "borrow" : borrow })
        borrow.reminded_borrower_pickup = True
        borrow.save()


def send_reminders_borrower_dropoff():
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    borrows = Borrow.objects.filter(
        state="ACCEPTED", finish=tomorrow, reminded_borrower_dropoff=False
    )
    for borrow in borrows:
        emails = _borrower_emails(borrow)
        subject, message = _get_email_templates("borrower", "remind_dropoff")
        send_mail(emails, subject, message, { "borrow" : borrow })
        borrow.reminded_borrower_dropoff = True
        borrow.save()


def send_reminders_lender_putout():
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    borrows = Borrow.objects.filter(
        state="ACCEPTED", start=tomorrow, reminded_lender_putout=False
    )
    for borrow in borrows:
        email = account_control.get_email_or_404(borrow.src.responsible)
        subject, message = _get_email_templates("lender", "remind_putout")
        send_mail([email], subject, message, { "borrow" : borrow })
        borrow.reminded_lender_putout = True
        borrow.save()


def send_reminders_lender_takein():
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    borrows = Borrow.objects.filter(
        state="ACCEPTED", finish=tomorrow, reminded_lender_takein=False
    )
    for borrow in borrows:
        email = account_control.get_email_or_404(borrow.dest.responsible)
        subject, message = _get_email_templates("lender", "remind_takein")
        send_mail([email], subject, message, { "borrow" : borrow })
        borrow.reminded_lender_takein = True
        borrow.save()


