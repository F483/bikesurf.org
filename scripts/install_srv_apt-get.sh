#!/bin/bash
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 

if [ "$(whoami)" != "root" ]; then
    echo "You don't have sufficient privileges!"
    exit 1
fi

# required apt packages
apt-get -qy install mercurial python-pip gettext
apt-get -qy install apache2 postgresql libapache2-mod-wsgi python-imaging python-psycopg2
apt-get -qy install python-django python-django-south # XXX only because i cant use pip stuff

# python packages
#pip install Django # incompatible with South ...
#pip install South  # incompatible with Django ...
pip install django-countries
pip install django-allauth
pip install django-html_sanitizer
pip install django-imagekit
pip install unidecode
pip install django-rosetta
pip install python-dateutil

hg clone https://bitbucket.org/fabe/bikesurf.org www
chown bikesurf:bikesurf -R bikesurfing.org/

# TODO setup database

# setup apache
cp www/config/apache_live.vh /etc/apache2/sites-available/bikesurf.org_live
cp www/config/apache_maintenance.vh /etc/apache2/sites-available/bikesurf.org_maintenance
ln -s /etc/apache2/sites-available/bikesurf.org_maintenance /etc/apache2/sites-enabled/bikesurf.org
/etc/init.d/apache2 restart

