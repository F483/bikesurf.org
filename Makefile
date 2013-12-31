
APP=""
SQLITE_FILE="uploads/development.db"

help:
	@echo "Usage: make <target> <option>=VALUE"
	@echo "  TARGETS                OPTIONS   "
	@echo "  runserver                        "
	@echo "  py_shell                         "
	@echo "  db_sync                          "
	@echo "  db_migration_create    APP       "
	@echo "  db_migration_apply     APP       "
	@echo "  db_shell_sqlite                  "
	@echo "  db_sql                 APP       "
	@echo "  clean                            "
	@echo "  makemessages                     "
	@echo "  compilemessages                  "

runserver:
	python manage.py runserver

db_sql:
	python manage.py sql $(APP)

db_shell_sqlite:
	sqlite3 $(SQLITE_FILE)

db_migration_create:
	python manage.py schemamigration $(APP) --auto

db_migration_apply:
	python manage.py migrate $(APP)

db_sync:
	python manage.py syncdb

py_shell:
	python manage.py shell

makemessages:
	scripts/messages.sh makemessages

compilemessages:
	scripts/messages.sh compilemessages

clean:
	find | grep -i ".*\.pyc$$" | xargs -r -L1 rm
	find | grep -i ".*\.orig$$" | xargs -r -L1 rm
	find | grep -i ".*\.swp$$" | xargs -r -L1 rm
	find | grep -i ".*\.swo$$" | xargs -r -L1 rm

