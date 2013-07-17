
APP=""
SQLITE_FILE="uploads/development.db"

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
	sqlite3 $(SQLITE_FILE)

db_sync: clean
	python manage.py syncdb

py_shell:
	python manage.py shell

makemessages:
	scripts/messages.sh makemessages

compilemessages:
	scripts/messages.sh compilemessages

clean:
	test -f $(SQLITE_FILE) && rm $(SQLITE_FILE) || echo ""
	find | grep -i ".*\.pyc$$" | xargs -r -L1 rm
	find | grep -i ".*\.orig$$" | xargs -r -L1 rm
	find | grep -i "uploads/.*\.jpeg$$" | xargs -r -L1 rm
	find | grep -i ".*\.po$$" | xargs -r -L1 rm
	find | grep -i ".*\.mo$$" | xargs -r -L1 rm

