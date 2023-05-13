import requests

import datetime

from newssentiment.production.news_predictor import NewsSentimentPredict

def main():
    symbol = 'AAPL'

    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    nsp = NewsSentimentPredict(symbol)

    prediction = {
            'datetime': date_now,
            'news_sentiment_polarity': nsp.to_dict()['news_sentiment_polarity'],
            'news_volume': nsp.to_dict()['news_volume'],
            'close_price_previous': nsp.to_dict()['close_price_previous'],
            'close_price_next_predicted': nsp.to_dict()['close_price_next_predicted'],
            'stock_symbol': symbol
            }
    
    print(prediction)

    base_url = 'http://127.0.0.1:5001/api/v1'
    r = requests.post(
            base_url + '/predictions/news',
            json=prediction)

    print(r.text)

if __name__ == "__main__":
    main()
