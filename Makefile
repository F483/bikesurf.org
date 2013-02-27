
APP=""

help:
	@echo "Usage: make <target> <option>=VALUE"
	@echo "  TARGETS            OPTIONS       "
	@echo "  runserver                        "
	@echo "  py_shell                         "
	@echo "  db_shell                         "
	@echo "  db_sync                          "
	@echo "  db_sql             APP           "
	@echo "  clean                            "

runserver:
	python manage.py runserver

db_sql:
	python manage.py sql $(APP)

db_shell:
	sqlite3 uploads/development.db

db_sync:
	test -f uploads/development.db && rm uploads/development.db || echo ""
	python manage.py syncdb

py_shell:
	python manage.py shell

clean:
	rm $$(find | grep -i ".*\.pyc$$")

