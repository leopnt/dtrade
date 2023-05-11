from typing import Optional
import numpy as np
import pandas as pd


class AscendingTriangles:
    def __init__(self, stock: np.array, ascending_triangles: np.array) -> None:
        self.raw_static_data_file = "./XNAS-APPL.csv"
        self.stock = stock
        self.ascending_triangles = ascending_triangles

    def import_static_csv_data(self) -> np.array():
        self.stock = pd.read_csv(
            self.raw_static_data_file, parse_dates=[0]
        )  # parse dates convert from str to date, [0] is col index
        self.stock.columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "adjustment_factor",
            "adjustment_type",
        ]
        return self.stock

    def clean_data(self, stock: np.array()):
        # delete days with no volume (weekends or public holiday)
        stock = stock[stock["volume"] != 0]
        stock.reset_index(drop=True, inplace=True)
        # Not needed and full of NaN values
        stock.drop(columns=["adjustment_factor", "adjustment_type"])

    def pivot_id(self, df, candle, before_candle, after_candle) -> int:
        """
        Calculate the pivot points and their direction.
        Returns 0 if the candlestick is not a pivot point,
        1 if it is a low pivot point, 2 if it is a high pivot point
        and 3 if it is a low and high pivot point at the same time.
        """
        if candle - before_candle < 0 or candle + after_candle >= len(df):
            return 0

        pividlow = 1
        pividhigh = 1
        for i in range(candle - before_candle, candle + after_candle + 1):
            if df.low[candle] > df.low[i]:
                pividlow = 0
            if df.high[candle] < df.high[i]:
                pividhigh = 0
        if pividlow and pividhigh:
            return 3
        elif pividlow:
            return 1
        elif pividhigh:
            return 2
        else:
            return 0

    def pointpos(self, x) -> float:
        """
        Calculate the value of the pivot point
        """
        if x["pivot"] == 1:
            return x["low"] - 1e-3
        elif x["pivot"] == 2:
            return x["high"] + 1e-3
        else:
            return np.nan

    """
    DEPRECATED
    Calcul si les points sont alignés à partir d'un np.array

    def is_horizontally_aligned(
        point: float, reference_points: np.array, accuracy: float = 0.03
    ) -> bool:
        "
        Returns true if the point is horizontaly aligned (+- 3% or accuracy) with the reference points
        "
        # calculate the average value of the reference pivot points
        if reference_points.size == 0:
            return True
        if (sum(reference_points) / len(reference_points) >= point * (1 - accuracy)) and (
            sum(reference_points) / len(reference_points) <= point * (1 + accuracy)
        ):
            return True
        else:
            return False
    """

    def mean(self, df: pd.DataFrame, reference_points_ids: np.array):
        sum = 0
        for i in range(len(reference_points_ids)):
            sum += df.iloc[i]
        return sum / len(reference_points_ids)

    def is_horizontally_aligned(
        self,
        df: pd.DataFrame,
        point_id: int,
        reference_points_ids: np.array,
        accuracy: float = 0.03,
    ) -> bool:
        """
        Returns true if the point is horizontaly aligned (+- 3% or accuracy) with the reference points ids
        """
        # calculate the average value of the reference pivot points
        if reference_points_ids.size == 0:
            return True
        if (
            self.mean(df, reference_points_ids) >= df.iloc[point_id] * (1 - accuracy)
        ) and (
            sum(reference_points_ids) / len(reference_points_ids)
            <= df.iloc[point_id] * (1 + accuracy)
        ):
            return True
        else:
            return False

    def get_plates(
        self, df: pd.DataFrame, pivot_type: int, last_candle_id: int, max_lookup: int
    ) -> Optional(np.array):
        """
        Returns a np.array containing the ids of the 3 points foring a plate in the interval between 'candle_id' and 'max_lookup'
        None if none was found
        """
        plate_points_ids = np.array([])
        i = 0
        for i in range(last_candle_id, last_candle_id - max_lookup):
            if df.iloc[i].pivot == pivot_type:
                if self.is_horizontally_aligned(df, plate_points_ids):
                    # upper_pivot_points_values.append(df.iloc[i].pointpos)
                    plate_points_ids.append(i)
            i += 1

        if len(plate_points_ids) < 3:
            return None

        return plate_points_ids

    def get_opposite_pivot_points(
        self, df: pd.DataFrame, pivot_type: int, last_candle_id: int, max_lookup: int
    ) -> np.array:
        opposite_pivot_points_ids = np.array([])
        for id in range(last_candle_id, int(last_candle_id - (1.5 * max_lookup))):
            if pivot_type == 2:
                if df.iloc[id].pivot == 1:
                    opposite_pivot_points_ids.append(id)
            if pivot_type == 1:
                if df.iloc[id].pivot == 2:
                    opposite_pivot_points_ids.append(id)
            id += 1
        return opposite_pivot_points_ids

    def is_ascending(df: pd.DataFrame, points_ids: np.array) -> bool:
        for i in len(points_ids) - 1:
            if df.iloc[points_ids[i]].value < df.iloc[points_ids[i]].value:
                return True
        return False

    def find_ascending_triangles(
        self, df: pd.DataFrame, last_candle_id: int, max_lookup: int
    ):
        """
        Returns all the ascending triangles found.
        Triangles needs to have at least 2 upper pivot points and 2 lower pivot points
        The search is made by window wich are the size of max_lookup.
        All triangles might not if some of them are positioned between 2 serach windows
        """
        while last_candle_id - max_lookup > 0:
            if last_candle_id > max_lookup:
                raise Exception(
                    "Error: max_lookup shoul be smaller than the last candle id"
                )

            # find all upper plates of minimum 3 upper pivot points
            # pivot_type = 2 correpond to upper pivot points
            upper_pivot_points_ids = self.get_plates(
                df=df,
                pivot_type=2,
                last_candle_id=last_candle_id,
                max_lookup=max_lookup,
            )

            # TODO: Remove this line if not necessary (we find lower pivot point with another method)
            # lower_pivot_points_ids = get_plates(df=df, pivot_type=1, last_candle_id=last_candle_id, max_lookup=1.5 * max_lookup)

            # Get all the lower pivot points located under the plate formed by the 3 upper pivot points
            lower_pivot_points_ids = self.get_opposite_pivot_points(
                df,
                pivot_type=2,
                last_candle_id=last_candle_id,
                max_lookup=1.5 * max_lookup,
            )

            # Checking that the lower pivot points are forming an ascending line
            if (len(lower_pivot_points_ids) >= 3) and self.is_ascending(
                df, lower_pivot_points_ids
            ):
                self.ascending_triangles.append(
                    [upper_pivot_points_ids, lower_pivot_points_ids]
                )

            last_candle_id = last_candle_id - max_lookup
