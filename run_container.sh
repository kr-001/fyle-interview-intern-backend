# SCRIPT FOR RUNNING THE CONTAINER

# set env variable
export FLASK_APP=core/server.py

#remove sqlite db
rm core/store.sqlite3

#apply migrations
flask db upgrade -d core/migrations/

## Run the Flask app
flask run --host 0.0.0.0 &

#test coverage 
pytest --cov