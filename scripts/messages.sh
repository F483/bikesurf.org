#!/bin/bash

ROOT=$PWD
COMMAND=$1
APPS=$(find apps/ -maxdepth 1 -type d | tail -n +2 | sort)
LANGS=$(python scripts/listlangs.py)

if [ "$COMMAND" != "makemessages" ] && [ "$COMMAND" != "compilemessages" ]; then
    echo "Usage: $0 <COMMAND>"
    echo "  makemessages: to generates po files."
    echo "  compilemessages: to generate mo files"
    exit 1
fi

for app in $APPS ; do
    for lang in $LANGS ; do
        mkdir -p "$ROOT/$app/locale"
        cd "$ROOT/$app"
        python ../../manage.py $COMMAND -l $lang
        cd "$ROOT"
    done
done

