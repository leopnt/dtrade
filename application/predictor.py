import requests

import datetime

from newssentiment.production.news_predictor import NewsSentimentPredict
from technicalanalysis.GetTriangleAscendant import TriangleAscendantData

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

    tad = TriangleAscendantData(symbol)

    # patch datetime
    target_date = tad.to_dict()['target_date']
    # +24 hours by default
    target_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
    if target_date:
        target_datetime = target_date

    # patch target_price
    target_price = tad.to_dict()['target_price']
    if not target_price:
        target_price = 0.0

    prediction = {
            'datetime': date_now,
            'delta_price_predicted': target_price,
            'target_datetime': target_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'stock_symbol': symbol,
            }

    print(prediction)

    base_url = 'http://127.0.0.1:5001/api/v1'

    r = requests.post(
            base_url + '/predictions/technical',
            json=prediction)

    print(r.text)

if __name__ == "__main__":
    main()
