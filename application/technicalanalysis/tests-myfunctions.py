from GetTriangleAscendant import TriangleAscendantData
import datetime


triangle = TriangleAscendantData("AAPL")
if triangle.target_price is not None:
    print("Objectif de prix : ", triangle.target_price)
    print("Date cible : ", triangle.target_date)
    today = datetime.today().strftime("%Y-%m-%d")
    if triangle.is_favorable_day(today):
        print("Journée favorable pour investir.")
    else:
        print("Journée non favorable pour investir.")
else:
    print("Pas de formation de triangle ascendant détectée.")
