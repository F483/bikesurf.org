
APP=""
SQLITE_FILE="uploads/development.db"

help:
	@echo "Usage: make <target> <option>=VALUE"
	@echo "  TARGETS                OPTIONS   "
	@echo "  runserver                        "
	@echo "  shell                            "
	@echo "  db_sync                          "
	@echo "  clean                            "
	@echo "  messages                         "

runserver:
	python manage.py runserver

db_sync:
	python manage.py syncdb

shell:
	python manage.py shell

messages:
	scripts/messages.sh makemessages
	scripts/messages.sh compilemessages

clean:
	find | grep -i ".*\.pyc$$" | xargs -r -L1 rm
	find | grep -i ".*\.swp$$" | xargs -r -L1 rm
	find | grep -i ".*\.swo$$" | xargs -r -L1 rm

