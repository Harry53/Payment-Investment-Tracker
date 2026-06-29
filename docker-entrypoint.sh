#!/usr/bin/env sh
set -eu

flask --app wsgi.py db upgrade
exec "$@"
