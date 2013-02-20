# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from apps.team.models import Team
from apps.blog.models import Blog
from apps.account.models import Account
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.blog.forms import CreateBlogForm


@require_http_methods(["GET"])
def list(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    blogs = Blog.objects.filter(team=team)
    return rtr(team, "blog", request, "blog/list.html", { "blogs" : blogs })


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):

    # get data
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)

    if request.method == "POST":
        form = CreateBlogForm(request.POST)
        if form.is_valid():

            # save blog
            blog = Blog()
            blog.team = team
            blog.name = form.cleaned_data["name"]
            blog.content = form.cleaned_data["content"]
            blog.created_by = account
            blog.updated_by = account
            blog.save()

            # TODO send messages

            return HttpResponseRedirect("/%s/blog" % team.link)
    else:
        form = CreateBlogForm()
    args = { "form" : form, "form_title" : _("ADD_BLOG") }
    return rtr(team, "blog", request, "common/form.html", args)


