# Bikesurf.org

A website for bike sharing.

# Installation for development

bikesurf.org is made with python/django.

### Dependencies for ubuntu

    # install apt packages
    sudo apt-get -qy install gettext libjpeg-dev

### Project Setup

    # Clone repository
    cd where/you/keep/your/repos
    git clone https://github.com/F483/bikesurf.org
    cd bikesurf.org

    # python virtualenv
    virtualenv -p /usr/bin/python2 env  # create virtualenv
    source env/bin/activate             # activate virtualenv

    # Install python packages
    python setup.py develop

    # Setup development database
    python manage.py syncdb

    # Start development server
    python manage.py runserver

