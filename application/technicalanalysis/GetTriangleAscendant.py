import yfinance as yf
import numpy as np


class TriangleAscendantData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = yf.download(ticker, period="1y", interval="1d")
        self.high = self.data["High"].values
        self.low = self.data["Low"].values
        self.close = self.data["Close"].values
        self.target_price = None
        self.target_date = None
        self.detect()

    def detect(self):
        n = len(self.close)
        highs = []
        lows = []
        for i in range(1, n):
            if self.high[i] > self.high[i - 1]:
                highs.append(i)
            elif self.low[i] < self.low[i - 1]:
                lows.append(i)
            lines = []
            for high in highs:
                for low in lows:
                    if high > low:
                        slope = (self.high[high] - self.low[low]) / (high - low)
                        line = [slope, self.high[high] - slope * high]
                        if all(
                            self.low[low:high] < slope * np.arange(low, high) + line[1]
                        ) and all(
                            self.high[low:high] > slope * np.arange(low, high) + line[1]
                        ):
                            lines.append(line)
            if len(lines) > 0:
                target_price = max(line[1] for line in lines)
                target_date = self.data.index[self.data["High"] == target_price][
                    0
                ].strftime("%Y-%m-%d")
                self.target_price = target_price
                self.target_date = target_date

    def is_favorable_day(self, date):
        date_index = np.where(self.data.index == np.datetime64(date))[0][0]
        last_3_days = self.data.iloc[date_index - 3 : date_index]
        if len(last_3_days) < 3:
            return False
        if all(last_3_days["High"] >= self.target_price):
            return True
        return False

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "target_price": self.target_price,
            "target_date": self.target_date,
        }
