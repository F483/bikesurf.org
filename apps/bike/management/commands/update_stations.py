# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.management.base import NoArgsCommand, CommandError
from apps.bike import control


class Command(NoArgsCommand):

    help = 'Updates bike.station for borrows that have ended.'

    def handle_noargs(self, *args, **options):
        control.update_stations()


