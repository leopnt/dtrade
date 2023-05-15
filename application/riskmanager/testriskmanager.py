from RiskManager import *

# Exemple d'utilisation
technical_analysis_prediction = {
    "datetime": "13052023",
    "predicted_price": 175.34,
    "target_datetime": "18052023",
    "stock_symbol": "AAPL",
    "valuable_day": True,
}

news_analysis_prediction = {
    "datetime": "13052023",
    "news_sentiment_analysis": 0.963,
    "news_volume": 113,
    "close_price_previous": 172.57,
    "close_price_predicted": 173.12,
    "stocke_symbol": "AAPL",
}

risk_manager = RiskManager(
    "AAPL", technical_analysis_prediction, news_analysis_prediction
)
print("Profitable Trade ?:", risk_manager.is_profitable_trade())
