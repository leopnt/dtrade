from flask import Flask, json, request, jsonify, g  # added to top of file
from flask_cors import CORS  # added to top of file

import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE = 'users.db'


def sqlite_error_template(e: sqlite3.Error) -> dict:
    return {"code": e.sqlite_errorcode,
            "name": e.sqlite_errorname,
            "msg": str(e)}


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts

    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/api/v1/users',  methods=['GET'])
def api_get_users():
    data = query_db('SELECT * FROM users')

    if data is None:
        return "cannot get users", 404

    return jsonify(data)


@app.route('/api/v1/users',  methods=['POST'])
def api_add_user():
    r = request.json

    if r is None:
        return "cannot insert user {}".format(r), 500

    try:
        data = query_db("INSERT INTO users (username, password_hash, email)\
                        VALUES (?,?,?)",
                        (r["username"], r["password_hash"], r["email"]))
    except sqlite3.Error as e:
        return sqlite_error_template(e), 500

    return jsonify(data)


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    user = query_db('SELECT * FROM users WHERE id=?', (user_id), one=True)

    if user is None:
        return "no such user", 404

    return jsonify(user)


@app.route('/api/v1/users/<user_id>',  methods=['DELETE'])
def api_delete_user(user_id):
    try:
        data = query_db("DELETE from users WHERE id=?", (user_id))
    except sqlite3.Error as e:
        return sqlite_error_template(e), 500

    return jsonify(data)


if __name__ == "__main__":
    with app.app_context():
        app.run()
