#!/bin/bash

apt-get install mercurial python-pip sqlite3 ipython
# TODO dont ask options

pip install Django
pip install django-countries
pip install django-social-auth

hg clone https://fabe@bitbucket.org/fabe/bikesurfing.org

# TODO set correct permissions for bikesurfing.org folder

