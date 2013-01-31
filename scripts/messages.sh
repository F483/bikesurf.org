#!/bin/bash

ROOT=$PWD
COMMAND=$1

if [ "$COMMAND" != "makemessages" ] && [ "$COMMAND" != "compilemessages" ]; then
    echo "Usage: $0 <COMMAND>"
    echo "  makemessages: to generates po files."
    echo "  compilemessages: to generate mo files"
    exit 1
fi

for lang in $(cat scripts/langs.txt) ; do
    for app in $(cat scripts/apps.txt) ; do
        mkdir -p "$ROOT/apps/$app/locale"
        cd "$ROOT/apps/$app"
        python ../../manage.py $COMMAND -l $lang
        cd "$ROOT"
    done
done

