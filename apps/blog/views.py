# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from apps.team.models import Team
from apps.blog.models import Blog
from apps.blog import control
from apps.team import control as team_control
from apps.account.models import Account
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.blog import forms
from django.forms import Form


@require_http_methods(["GET"])
def listing(request, team_link):
    team = team_control.get_or_404(team_link)
    blogs = Blog.objects.filter(team=team)
    return rtr(team, "blog", request, "blog/list.html", { "blogs" : blogs })


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = forms.Create(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            blog = control.create(account, team, name, content)
            return HttpResponseRedirect("/%s/blog" % team.link)
    else:
        form = forms.Create()
    args = { 
        "form" : form, "form_title" : _("ADD_BLOG"), 
        "cancel_url" : "/%s" % team.link
    }
    return rtr(team, "blog", request, "site/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request, team_link, blog_id):

    # get data
    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    blog = get_object_or_404(Blog, team=team, id=blog_id)
    assert_member(account, team)

    if request.method == "POST":
        form = forms.Edit(request.POST, blog=blog)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            control.edit(account, blog, name, content)
            return HttpResponseRedirect("/%s/blog" % (team.link))
    else:
        form = forms.Edit(blog=blog)
    args = { 
        "form" : form, "form_title" : _("BLOG_EDIT"), 
        "cancel_url" : "/%s" % team.link
    }
    return rtr(team, "blog", request, "site/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def delete(request, team_link, blog_id):

    # get data
    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    blog = get_object_or_404(Blog, team=team, id=blog_id)
    assert_member(account, team)

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            control.delete(account, blog)
            return HttpResponseRedirect("/%s/blog" % team.link)
    else:
        form = Form()
    args = { 
        "form" : form, "form_title" : _("BLOG_DELETE?"), 
        "form_subtitle" : blog.name, "cancel_url" : "/%s/blog" % team.link
    }
    return rtr(team, "blog", request, "site/form.html", args)


