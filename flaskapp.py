from flask import Flask
# from flask_cors import CORS, cross_origin
import psycopg2
import psycopg2.extras

# import configuration
from helpers import json_response

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_pyfile('flaskapp.cfg')
configuration = {}
configuration.postgres_credentials = app.config['POSTGRES']


@app.route('/')
def hello_word():
    return 'Hello World'


@app.route('/api/actor/<actor_id>/genre_rating')
@json_response
def actor_genre_rating(actor_id):
    conn = psycopg2.connect(configuration.postgres_credentials)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SET search_path TO light")
    cur.execute('SELECT * from "CF_get_actor_genre_rating"(%s)' % actor_id)
    rows = cur.fetchall()
    return rows


@app.route('/api/actor/<actor_id>/movies')
@json_response
def actor_movies(actor_id):
    conn = psycopg2.connect(configuration.postgres_credentials)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SET search_path TO light")
    cur.execute('SELECT * from "CF_get_actor_movies"(%s)' % actor_id)
    rows = cur.fetchall()
    return rows


@app.route('/api/actor/<actor_id>')
@json_response
def actor(actor_id):
    conn = psycopg2.connect(configuration.postgres_credentials)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SET search_path TO light")
    cur.execute('SELECT actor.id id, actor.gender gender, fname.name fname, lname.name lname from '
                'actor JOIN actor_name lname '
                'ON lname.id = lname_id '
                'JOIN actor_name fname '
                'ON fname.id = fname_id '
                'WHERE actor.id = %s' % actor_id)
    rows = cur.fetchall()
    return rows[0]


@app.route('/api/actor/list')
@json_response
def actor_list():
    conn = psycopg2.connect(configuration.postgres_credentials)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SET search_path TO light")
    cur.execute("SELECT actor.id, fname.name fname, lname.name lname, "
                "fname.name || ' ' || lname.name full_name, actor.gender "
                "FROM actor "
                "JOIN actor_name fname ON fname_id = fname.id "
                "JOIN actor_name lname ON lname_id = lname.id")
    rows = cur.fetchall()
    return rows
