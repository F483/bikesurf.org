# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.forms import Form
from apps.account.models import Account
from apps.gallery.models import Gallery
from apps.gallery.models import Picture
from apps.team.utils import render_team_response as rtr
from apps.common.shortcuts import render_response
from apps.team.models import Team
from apps.gallery import forms
from apps.gallery import control
from apps.team.utils import assert_member


@login_required
@require_http_methods(["GET", "POST"])
def add(request, **kwargs):
    team_link = kwargs.get("team_link")
    gallery_id = kwargs["gallery_id"]
    account = get_object_or_404(Account, user=request.user)
    gallery = get_object_or_404(Gallery, id=gallery_id)
    team = team_link and get_object_or_404(Team, link=team_link) or None
    if team:
        assert_member(account, team)
    if request.method == "POST":
        form = forms.Add(request.POST, request.FILES)
        if form.is_valid():
            picture = control.add(account, form.cleaned_data["image"], gallery)
            prefix = team_link and "/%s" % team_link or ""
            url = "%s/gallery/view/%s" % (prefix, picture.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Add()
    args = { 
        "form" : form, "form_title" : _("ADD_PICTURE_TO_GALLERY"), 
        "multipart_form" : True 
    }
    if team:
        return rtr(team, None, request, "common/form.html", args)
    else:
        return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def setprimary(request, **kwargs):
    team_link = kwargs.get("team_link")
    picture_id = kwargs["picture_id"]
    account = get_object_or_404(Account, user=request.user)
    team = team_link and get_object_or_404(Team, link=team_link) or None
    picture = get_object_or_404(Picture, id=picture_id)
    prefix = team_link and "/%s" % team_link or ""
    url = "%s/gallery/list/%s" % (prefix, picture.gallery.id)
    if team:
        assert_member(account, team)
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            control.setprimary(account, picture)
            return HttpResponseRedirect(url)
    else:
        form = Form()
    # TODO make template that shows the image being set!
    args = { 
        "form" : form, "form_title" : _("SET_AS_PRIMARY_PICTURE"), 
        "cancle_url" : url
    }
    if team:
        return rtr(team, None, request, "common/form.html", args)
    else:
        return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def remove(request, **kwargs):
    team_link = kwargs.get("team_link")
    picture_id = kwargs["picture_id"]
    team = team_link and get_object_or_404(Team, link=team_link) or None
    picture = get_object_or_404(Picture, id=picture_id)
    gallery = picture.gallery
    account = get_object_or_404(Account, user=request.user)
    prefix = team_link and "/%s" % team_link or ""
    url = "%s/gallery/list/%s" % (prefix, gallery.id)
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            control.remove(account, picture)
            return HttpResponseRedirect(url)
    else:
        form = Form()
    args = { 
        "form" : form, "form_title" : _("REMOVE_GALLERY_PICTURE"), 
        "cancle_url" : url
    }
    if team:
        return rtr(team, None, request, "common/form.html", args)
    else:
        return render_response(request, "common/form.html", args)


@require_http_methods(["GET"])
def list(request, **kwargs):
    team_link = kwargs.get("team_link")
    gallery_id = kwargs["gallery_id"]
    team = team_link and get_object_or_404(Team, link=team_link) or None
    gallery = get_object_or_404(Gallery, id=gallery_id)
    pictures = gallery.pictures.all()
    args = { "gallery" : gallery, "pictures" : pictures }
    if team:
        return rtr(team, None, request, "gallery/list.html", args)
    else:
        return render_response(request, "gallery/list.html", args)


@require_http_methods(["GET"])
def view(request, **kwargs):
    team_link = kwargs.get("team_link")
    picture_id = kwargs["picture_id"]
    team = team_link and get_object_or_404(Team, link=team_link) or None
    picture = get_object_or_404(Picture, id=picture_id)
    args = { "picture" : picture }
    if team:
        return rtr(team, None, request, "gallery/view.html", args)
    else:
        return render_response(request, "gallery/view.html", args)


