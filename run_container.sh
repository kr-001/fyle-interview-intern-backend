#!/bin/bash

# Set environment variable
export FLASK_APP=core/server.py

# Remove SQLite database
rm core/store.sqlite3

# Apply database migrations
flask db upgrade -d core/migrations/

# Run Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:5000 core.server:app
