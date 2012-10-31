
APP=""

help:
	# COMMANDS          OPTIONS
	# server_start
	# db_sync
	# db_validate
	# db_sql            APP
	# app_create        APP
	# shell

server_start:
	python manage.py runserver

db_sync:
	python manage.py syncdb

db_validate:
	python manage.py validate

db_sql:
	python manage.py sql $(APP)

app_create:
	python manage.py startapp $(APP)

shell:
	python manage.py shell
