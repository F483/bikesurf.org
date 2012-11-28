
APP=""

help:
	@echo "Usage: make <target> <option>=VALUE"
	@echo "  TARGETS            OPTIONS       "
	@echo "  runserver                        "
	@echo "  py_shell                         "
	@echo "  db_shell                         "
	@echo "  db_sync                          "
	@echo "  db_sql             APP           "

runserver:
	python manage.py runserver

db_sql:
	python manage.py sql $(APP)

db_shell:
	sqlite3 data/development.db

db_sync:
	#rm data/development.db
	python manage.py syncdb

py_shell:
	python manage.py shell


