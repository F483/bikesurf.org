#!/bin/bash
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


if [ "$(whoami)" != "root" ]; then
    echo "You don't have sufficient privileges!"
    exit 1
fi


apt-get -qy install mercurial python-pip sqlite3

pip install Django
pip install django-countries
pip install django-social-auth

hg clone https://bitbucket.org/fabe/bikesurfing.org
chown ${USER}:${USER} -R bikesurfing.org/

