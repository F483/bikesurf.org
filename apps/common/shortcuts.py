# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from unidecode import unidecode
from django.db import models
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django_countries import countries
from django.shortcuts import _get_queryset
from django.template.loader import render_to_string
from django.core.mail import send_mail as _send_mail
from django.conf import settings
from config.settings import GOOGLE_ANALYTICS_URL, GOOGLE_ANALYTICS_ID


COUNTRIES = [('', '---------')] + list(countries.COUNTRIES)


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def uslugify(ustr):
    """ because slugify is shit with unicode """
    return slugify(unidecode(ustr))


def render_response(request, template, args):
    # avoid circular imports ...
    from apps.team import control as team_control 
    from apps.borrow import control as borrow_control
    from apps.borrow.models import Borrow
    from apps.station.models import Station

    args.update({ 
        "current_user" : request.user,
        "current_path" : request.path,
        "google_analytics_url" : GOOGLE_ANALYTICS_URL,
        "google_analytics_id" : GOOGLE_ANALYTICS_ID,
    })
    if request.user.is_authenticated():
        account = request.user.accounts.all()[0]
        borrows = Borrow.objects.filter(borrower=account)
        borrows = borrows.exclude(state="CANCELED").exclude(state="FINISHED")
        args.update({ 
            "current_account" : account,
            "borrow_count" : len(borrows),
            "current_account_teams" : team_control.get_teams(account),
            "station_count" : len(Station.objects.filter(responsible=account)),
            "departure_count" : len(borrow_control.departures(account)),
            "arrival_count" : len(borrow_control.arrivals(account)),
        })
    args.update(csrf(request))
    return render_to_response(template, args)


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def send_mail(recipient_list, template_subject, template_message, context):
    # TODO add i18n templates for users prefered language
    # TODO use async mail queue
    site = context["site"] = Site.objects.get_current()
    sender = settings.EMAIL_HOST_USER
    subject = render_to_string(template_subject, context) # render subject
    subject = u" ".join(subject.splitlines()).strip() # remove newlines
    subject = u"[{site}] {subject}".format(site=site.name, subject=subject) # add prefix
    message = render_to_string(template_message, context).strip()
    return _send_mail(subject, message, sender, recipient_list)


