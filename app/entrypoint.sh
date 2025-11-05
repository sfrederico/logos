#!/bin/sh
set -e

if [ "$DEBUG" = "True" ]; then
        echo "Running Flask in development mode..."
        exec flask --app src.app run --host=0.0.0.0 --port=5000
else
        echo "Running Flask in production mode..."
        exec gunicorn -w 2 -b 0.0.0.0:5000 src.app:app
fi
