<VirtualHost *:80>
    ServerAdmin fabian.barkhau@gmail.com
    ServerName  bikesurf.org
    ServerAlias www.bikesurf.org
    
    DocumentRoot /home/bikesurf/www
 
    # mod_wsgi settings
    #WSGIDaemonProcess bikesurf python-path=/home/bikesurf/www:/usr/lib/python2.7:/usr/lib/python2.7/plat-linux2:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/PIL
    WSGIDaemonProcess bikesurf user=bikesurf group=bikesurf python-path=/home/bikesurf/www:/usr/lib/python2.7:/usr/lib/python2.7/plat-linux2:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/PIL

    WSGIProcessGroup bikesurf
    WSGIScriptAlias / /home/bikesurf/www/config/wsgi.py
 
    # static media aliases
    Alias /static/ /home/bikesurf/www/static/
    Alias / /home/bikesurf/www/apps/site/templates/site/maintenance.html
 
    # static permissions
    <Directory /home/bikesurf/www/static>
        Order deny,allow
        Allow from all
    </Directory>
 
    # media permissions
    <Directory /home/bikesurf/www/media>
        Order deny,allow
        Allow from all
    </Directory>
 
    # Project wsgi permissions
    # Used for serving django pages.
    <Directory /home/bikesurf/www/config>
        <Files wsgi.py>
            Order deny,allow
            Allow from all
        </Files>
    </Directory>

    # logging
    LogLevel warn 
    ErrorLog  /home/bikesurf/log/apache_error.log 
    CustomLog /home/bikesurf/log/apache_access.log combined 

</VirtualHost>
