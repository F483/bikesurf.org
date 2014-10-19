Bikesurfing.org
===============

A website for bike sharing.

Installation for development on ubuntu
======================================

    # install apt packages
    cd where/you/keep/your/repos
    sudo apt-get -qy install apache2 postgresql libapache2-mod-wsgi # only for server
    sudo apt-get -qy install gettext libjpeg-dev

    # Clone repository
    hg clone https://bitbucket.org/fabe/bikesurf.org
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
