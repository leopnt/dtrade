import yfinance

TOTAL_INVESTED = 10000
MAX_RISK_PER_TRADE = 5
FEE_PER_TRADE = 0.01


class RiskManager:
    def __init__(
        self, stock_symbol, technical_analysis_prediction, news_analysis_prediction
    ) -> None:
        self.stock_symbol = stock_symbol
        self.technical_analysis = technical_analysis_prediction
        self.news_analysis = news_analysis_prediction

    def get_current_stock_price(self) -> float:
        try:
            data = yfinance.download(self.stock_symbol, period="2d", interval="1d")
            return data["Close"][-1]
        except Exception:
            raise Exception("ERROR: the stock_symbol does not exist")

    def calculate_nb_stock(self) -> float:
        """
        Calculate the number of stock a user can buy based on his
        total amount invested and his maximum risk per trade
        """
        nb_stock = (
            (MAX_RISK_PER_TRADE * TOTAL_INVESTED) / 100
        ) / self.get_current_stock_price()

        if nb_stock >= 1:
            return int(nb_stock)
        else:
            return 0

    def is_profitable_trade(self):
        """
        Check if the given prediction respects the risk management rules
        """
        current_stock_price = self.get_current_stock_price()
        print("current_stock_price :", current_stock_price)

        nb_stock = self.calculate_nb_stock()
        print("nb_stock :", nb_stock)

        potential_gain = (
            self.news_analysis.get("close_price_next_predicted") - current_stock_price
        ) * nb_stock
        print("potentiel gain :", potential_gain)
        print("FEE_PER_TRADE*2 :", FEE_PER_TRADE * 2)
        if potential_gain > FEE_PER_TRADE * 2:
            # patch valuable_day not in DB
            return True

            if self.technical_analysis.get("valuable_day"):
                return True
            elif (
                self.news_analysis.get("predicted_stock_price") - current_stock_price
            ) * nb_stock > 20 * FEE_PER_TRADE:
                return True
        return False
