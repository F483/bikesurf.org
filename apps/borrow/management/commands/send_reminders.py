# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.management.base import NoArgsCommand, CommandError
from apps.borrow import control


class Command(NoArgsCommand):

    help = 'Send reminder emails.'

    def handle_noargs(self, *args, **options):
        control.send_reminders_borrower_rate()
        control.send_reminders_borrower_pickup()
        control.send_reminders_borrower_dropoff()
        control.send_reminders_lender_putout()
        control.send_reminders_lender_takein()


