from flask import Flask, json, request, jsonify, g  # added to top of file
from flask_cors import CORS  # added to top of file

import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE = "users.db"


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("PRAGMA foreign_keys = ON")

    db.row_factory = make_dicts

    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/api/v1/users", methods=["GET"])
def api_get_users():
    data = query_db("SELECT * FROM users")

    if data is None:
        return "cannot get users", 404

    return jsonify(data)


@app.route("/api/v1/users", methods=["POST"])
def api_add_user():
    r = request.json

    if not r:
        return "cannot insert user: empty json body", 400

    if (
        not r["username"]
        or not r["password_hash"]
        or not r["email"]
        or not r["total_invested"]
        or not r["max_risk_per_trade"]
        or not r["fee_per_trade"]
    ):
        return "cannot insert user: incomplete json body: {}".format(r), 400

    try:
        data = query_db(
            "INSERT INTO users (username, password_hash, email, total_invested, max_risk_per_trade, fee_per_trade)\
                        VALUES (?,?,?)",
            (
                r["username"],
                r["password_hash"],
                r["email"],
                r["total_invested"],
                r["max_risk_per_trade"],
                r["fee_per_trade"],
            ),
        )
    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


@app.route("/api/v1/users/<user_id>", methods=["GET"])
def api_get_user(user_id):
    user = query_db("SELECT * FROM users WHERE id=?", (user_id), one=True)

    return jsonify(user)


@app.route("/api/v1/users/<user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    try:
        data = query_db("DELETE FROM users WHERE id=?", (user_id))
    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


@app.route("/api/v1/alerts", methods=["GET"])
def api_get_user_alerts():
    user_id = request.args.get("user_id")

    try:
        if user_id:
            data = query_db("SELECT * FROM alerts WHERE user_id=?", (user_id))
        else:
            data = query_db("SELECT * FROM alerts")
    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


@app.route("/api/v1/alerts", methods=["POST"])
def api_add_alert():
    user_id = request.args.get("user_id")
    symbol_name = request.args.get("symbol_name")
    r = request.json

    if r is None:
        return "cannot add alert: empty json body", 400

    for required_key in [
        "title",
        "content",
        "type",
        "discord_webhook_url",
        "smtp_url",
        "email_addr",
        "ntfy_topic",
    ]:
        if required_key not in r.keys():
            return "cannot add alert: empty '{}'".format(required_key), 400

    try:
        data = query_db(
            "INSERT INTO alerts\
                        (symbol_name, user_id, title, content, type, discord_webhook_url, smtp_url, email_addr, ntfy_topic)\
                        VALUES (?,?,?,?,?,?,?,?,?)",
            (
                symbol_name,
                user_id,
                r["title"],
                r["content"],
                r["type"],
                r["discord_webhook_url"],
                r["smtp_url"],
                r["email_addr"],
                r["ntfy_topic"],
            ),
        )

    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


@app.route("/api/v1/alerts", methods=["DELETE"])
def api_delete_alert():
    symbol_name = request.args.get("symbol_name")
    user_id = request.args.get("user_id")

    try:
        data = query_db(
            "DELETE FROM alerts WHERE user_id=? AND symbol_name=?",
            (user_id, symbol_name),
        )
    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


if __name__ == "__main__":
    with app.app_context():
        app.run(host="127.0.0.1", port=8080)
