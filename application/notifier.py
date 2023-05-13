import requests

from riskmanager.RiskManager import RiskManager

USERS_BASE_API_URL = "http://127.0.0.1:5000/api/v1"
PREDICTIONS_BASE_API_URL = "http://127.0.0.1:5001/api/v1"

class Notification:
    def __init__(self, title: str, content: str):
        self.title = title 
        self.content = content

    def sendDiscord(self, webhook_url: str):
        raise NotImplemented

    def sendEmail(self, smtp_url: str):
        raise NotImplemented

    def sendNtfy(self, topic: str):
        requests.post("https://ntfy.sh/{}".format(topic),
                      data="{}"
                      .format(self.content)
                      .encode(encoding='utf-8'))

class Notifier:
    def __init__(self) -> None:
        pass

    def load_alerts(self, api_url):
        self.alerts = requests.get(api_url).json()

    def notify_all(self):
        for alert in self.alerts:
            try:
                stock_symbol = alert["symbol_name"]

                technical_analysis_prediction = requests.get(
                        PREDICTIONS_BASE_API_URL
                        + "/predictions/technical/"
                        + stock_symbol).json()

                # latest prediction
                news_sentiment_predictions = requests.get(
                        PREDICTIONS_BASE_API_URL
                        + "/predictions/news/"
                        + stock_symbol).json()

                riskManager = RiskManager(stock_symbol,
                                          technical_analysis_prediction[-1],
                                          news_sentiment_predictions[-1])

                if riskManager.is_profitable_trade():
                    notification = Notification(alert['title'], alert['content'])
                    notification.sendNtfy(alert['ntfy_topic'])

            except Exception as e:
                print("Warning: Cannot send notification for alert:", alert)

def main():
    n = Notifier()
    n.load_alerts(USERS_BASE_API_URL + "/alerts")
    n.notify_all()

if __name__ == "__main__":
    main()
