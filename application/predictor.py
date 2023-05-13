import requests
import yfinance
import json

SERVER_URL = "http://127.0.0.1:8080"


class UserPrameters:
    def __init__(self, id, total_invested, max_risk_per_trade, fee_per_trade):
        self.id = id
        self.total_invested = total_invested
        self.max_risk_per_trade = max_risk_per_trade
        self.fee_per_trade = fee_per_trade


class Prediction:
    def __init__(
        self,
        current_stock_price,
        news_predicted_stock_price,
        technical_predicted_stock_price,
        technical_target_datetime,
    ):
        self.current_stock_price = current_stock_price
        self.news_predicted_stock_price = news_predicted_stock_price
        self.technical_predicted_stock_price = technical_predicted_stock_price
        self.technical_target_datetime = technical_target_datetime


def get_technical_analysis(stock_symbol) -> json:
    url = f"{SERVER_URL}/api/v1/predictions/technical/{stock_symbol}"
    response = requests.get(url)
    return response.json()


def get_news_analysis(stock_symbol) -> json:
    url = f"{SERVER_URL}/api/v1/predictions/news/{stock_symbol}"
    response = requests.get(url)
    return response.json()


def get_user_params(user) -> UserPrameters:
    url = f"{SERVER_URL}/api/v1/users/{user.id}"
    response = requests.get(url)
    user_params = UserPrameters(
        response.get("id"),
        response.get("total_invested"),
        response.get("max_risk_per_trade"),
        response.get("fee_per_trade"),
    )
    return user_params


def get_current_stock_price(stock_symbol) -> float:
    try:
        data = yfinance.download(stock_symbol, period="2d", interval="1d")
        return data["Close"][-1]
    except Exception:
        raise Exception("ERROR: the stock_symbol does not exist")


def calculate_nb_stock(user, current_stock_price) -> float:
    """
    Calculate the number of stock a user can buy based on his
    total amount invested and his maximum risk per trade
    """
    nb_stock = (
        (user.max_risk_per_trade * user.total_invested) / 100
    ) / current_stock_price
    if nb_stock >= 1:
        return int(nb_stock)
    else:
        return 0


def is_profitable_trade(user, stock_symbol):
    user_params = get_user_params(user)
    technical_analysis = get_technical_analysis(stock_symbol)
    news_predict = get_news_analysis(stock_symbol)
    current_stock_price = get_current_stock_price(stock_symbol)
    nb_stock = calculate_nb_stock(user_params, current_stock_price)
    potential_gain = (
        news_predict.get("predicted_stock_price") - current_stock_price
    ) * nb_stock

    if potential_gain > user_params.fees_per_trade * 2:
        if technical_analysis.get("valuable_day"):
            return Prediction(
                current_stock_price,
                news_predict.get("predicted_stock_price"),
                technical_analysis.get("predicted_stock_price"),
                technical_analysis.get("target_datetime"),
            )
        elif (
            news_predict.get("predicted_stock_price") - current_stock_price
        ) * nb_stock > 20 * user_params.fee_per_trade:
            return Prediction(
                current_stock_price,
                news_predict.get("predicted_stock_price"),
                technical_analysis.get("predicted_stock_price"),
                technical_analysis.get("target_datetime"),
            )

    return None


def notify(user, stock_symbol):
    profitable_trade = is_profitable_trade(user, stock_symbol)
    if profitable_trade:
        notification = {
            "current_stock_price": profitable_trade.curren_stock_price,
            "news_predicted_stock_price": profitable_trade.news_predicted_stock_price,
            "technical_predicted_stock_price": profitable_trade.technical_predicted_stock_price,
            "technical_targer_datetime": profitable_trade.technical_target_datetime,
        }
        # Envoi de la notification
        print(notification)


# Exemple d'utilisation
user_params = UserPrameters(1, 10000, 2, 0.05)
notify(user_params, "AAPL")
