from flask import Flask, json, request, jsonify, g  # added to top of file
from flask_cors import CORS  # added to top of file

import sqlite3
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE = 'predictions.db'

def validate_iso8601(date_str: str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return False
    
    return True

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("PRAGMA foreign_keys = ON")

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


@app.route('/api/v1/predictions/technical/<stock_symbol>',  methods=['GET'])
def api_get_predictions_technical(stock_symbol):
    data = query_db(
        'SELECT * FROM technical_analysis_predict WHERE stock_symbol=?',
        (stock_symbol,))

    if data is None:
        return "cannot get technical analysis predictions", 404

    return jsonify(data)


@app.route('/api/v1/predictions/technical',  methods=['POST'])
def api_add_predictions_technical():
    r = request.json

    if not r:
        return "cannot insert prediction: empty json body", 400

    for required_key in ["datetime", "delta_price_predicted", "target_datetime",
                         "stock_symbol"]:
        if required_key not in r.keys():
            return "cannot add alert: empty '{}'".format(required_key), 400

    if not validate_iso8601(r["datetime"]):
        return "cannot insert prediction: invalid iso8601 datetime format", 400
    if not validate_iso8601(r["target_datetime"]):
        return "cannot insert prediction: invalid iso8601 datetime format", 400

    try:
        data = query_db("INSERT INTO technical_analysis_predict\
                        (datetime, delta_price_predicted, target_datetime,\
                        stock_symbol) VALUES (?,?,?,?)",
                        (r["datetime"], r["delta_price_predicted"],
                         r["target_datetime"], r["stock_symbol"]))
    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


@app.route('/api/v1/predictions/news/<stock_symbol>',  methods=['GET'])
def api_get_predictions_news(stock_symbol):
    data = query_db(
        'SELECT * FROM news_sentiment_predict WHERE stock_symbol=?',
        (stock_symbol,))

    if data is None:
        return "cannot get news sentiment predictions", 404

    return jsonify(data)


@app.route('/api/v1/predictions/news',  methods=['POST'])
def api_add_predictions_news():
    r = request.json

    if not r:
        return "cannot insert prediction: empty json body", 400

    for required_key in ["datetime", "news_sentiment_polarity", "news_volume",
                         "close_price_previous", "close_price_next_predicted",
                         "stock_symbol"]:
        if required_key not in r.keys():
            return "cannot add alert: empty '{}'".format(required_key), 400

    if not validate_iso8601(r["datetime"]):
        return "cannot insert prediction: invalid iso8601 datetime format", 400

    try:
        data = query_db("INSERT INTO news_sentiment_predict\
                        (datetime, news_sentiment_polarity, news_volume,\
                        close_price_previous, close_price_next_predicted,\
                        stock_symbol) VALUES (?,?,?,?,?,?)",
                        (r["datetime"], r["news_sentiment_polarity"],
                         r["news_volume"], r["close_price_previous"],
                         r["close_price_next_predicted"], r["stock_symbol"]))
    except sqlite3.Error as e:
        return str(e), 500

    return jsonify(data)


@app.route('/api/v1/stock_symbol/available',  methods=['GET'])
def api_get_stock_symbols_available():
    data = query_db('SELECT * FROM stock_symbol_available')

    if data is None:
        return "cannot get available stock symbols", 404

    return jsonify(data)


if __name__ == "__main__":
    with app.app_context():
        app.run()
