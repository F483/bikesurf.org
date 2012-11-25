
APP=""

help:
	@echo "Usage: make <target> <option>=VALUE"
	@echo "  TARGETS            OPTIONS       "
	@echo "  server_start                     "
	@echo "  db_sync                          "
	@echo "  db_validate                      "
	@echo "  db_dev_shell                     "
	@echo "  db_dev_sync                      "
	@echo "  db_sql             APP           "
	@echo "  app_create         APP           "
	@echo "  shell                            "
	@echo "  ubuntu_dev_env                   "

server_start:
	python manage.py runserver

db_sync:
	python manage.py syncdb

db_validate:
	python manage.py validate

db_sql:
	python manage.py sql $(APP)

db_dev_shell:
	sqlite3 db/development.db

db_dev_sync:
	rm db/development.db
	python manage.py syncdb

app_create:
	python manage.py startapp $(APP)

shell:
	python manage.py shell

ubuntu_dev_env:
	apt-get install python-pip sqlite3
	pip install Django
	pip install django-countries
	pip install django-social-auth



