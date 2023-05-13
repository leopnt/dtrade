from predictor import *

get_user_params_response = {
    "1": {
        "id": 1,
        "name": "John Doe 1",
        "total_invested": 10000,
        "max_risk_per_trade": 2,
        "fee_per_trade": 0.05,
    }
}

# Exemple d'utilisation
user_params = UserPrameters(1, 10000, 2, 0.05)
notify(user_params, "AAPL")
