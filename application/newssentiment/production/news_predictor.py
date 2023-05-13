#!python3

import os
import praw
import yfinance
import joblib
from textblob import TextBlob
from datetime import datetime


class News:
    def __init__(self, text: str = ""):
        self.text = text
    
    def ts_polarity(self) -> float:
        return TextBlob(self.text).sentiment.polarity
    
    def __str__(self) -> str:
        return "News({})".format(self.text)

    def __hash__(self) -> int:
        return hash(self.text)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)): return False
        return self.text == other.text

class NewsCache:
    def __init__(self) -> None:
        self.cache = set()
    
    def tweets(self):
        return self.cache

    def ts_polarity_mean(self) -> float:
        ts_polarity_sum = 0.0
        for tweet in self.tweets():
            ts_polarity_sum += tweet.ts_polarity()
        
        return ts_polarity_sum / float(self.volume())

    def push(self, news: News) -> None:
        self.cache.add(news)

    def clear(self) -> None:
        self.cache.clear()
    
    def volume(self) -> int:
        return len(self.cache)

class PricePredictor():
    def __init__(self) -> None:
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"

        self.model = joblib.load(
                PROJECT_ROOT + "../training/stock_prediction.joblib")
        self.x_scaler = joblib.load(
                PROJECT_ROOT + "../training/stock_prediction_x_scaler.joblib")
        self.y_scaler = joblib.load(
                PROJECT_ROOT + "../training/stock_prediction_y_scaler.joblib")

    def predict(
        self, stock_ticker: yfinance.Ticker, news_cache: NewsCache) -> dict:

        close_price = stock_ticker.info["previousClose"]

        X = [[
            news_cache.ts_polarity_mean(),
            news_cache.volume(),
            close_price
        ]]

        predicted = self.model.predict(self.x_scaler.transform(X))
        predicted_price = self.y_scaler.inverse_transform(
            predicted.reshape(-1, 1))
        
        return {
                'news_sentiment_polarity': news_cache.ts_polarity_mean(),
                'news_volume': news_cache.volume(),
                'close_price_previous': close_price,
                'close_price_next_predicted': float(predicted_price[0][0]),
                }

class NewsSentimentPredict:
    def __init__(self, symbol: str) -> None:
        news_cache = NewsCache()
        aapl_stock = yfinance.Ticker("AAPL")
        price_predictor = PricePredictor()
        reddit = praw.Reddit(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            user_agent=os.environ.get("USER_AGENT"))
        subreddit = reddit.subreddit('apple')

        for submission in subreddit.top(time_filter="day"):
            title = submission.title
            news_cache.push(News(title))

        self.prediction = price_predictor.predict(aapl_stock, news_cache)
        news_cache.clear()

    def to_dict(self):
        return self.prediction


def main():
    nsp = NewsSentimentPredict('AAPL')
    print("Predicted : {}".format(nsp.to_dict()))

if __name__ == "__main__":
    main()
