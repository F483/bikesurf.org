# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import settings


admin.autodiscover()


urlpatterns = patterns("",

    # admin
    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/", include(admin.site.urls)),

    # bikesurf urls
    url(r"^", include("apps.site.urls")),
    url(r"^", include("apps.station.urls")),
    url(r"^", include("apps.bike.urls")),
    url(r"^", include("apps.borrow.urls")),
    url(r"^", include("apps.team.urls")),
    url(r"^", include("apps.blog.urls")),
    url(r"^", include("apps.page.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

