import pandas as pd
import numpy as np
import scipy.stats as si
from liquer import *
import liquer.ext.lq_pandas

NORDEA_TICK = "CPH:NDA-DK"
DANSKE_TICK = "CPH:DANSKE"

@first_command
def create_portfolio():
    return pd.DataFrame([
        dict(asset_type="Equity", position=100.0, rf=NORDEA_TICK),
        dict(asset_type="Equity", position=10.0, rf=DANSKE_TICK),
        dict(asset_type="VanillaCallOption", position=1.0, rf=NORDEA_TICK, strike=70.0, maturity=10.0, interest_rate_rf="DKKLIBOR-1W"),
    ])

scenario = {
    "DAY": 1,
    "CPH:NDA-DK": 67.63,
    "CPH:DANSKE": 106.1,
    "CPH:NDA-DK-volatility": 1,
    "EONIA": -0.0049,
    "DKKLIBOR-1W": -0.00002,
}

scenario2 = {
    "DAY": 1,
    "CPH:NDA-DK": 70,
    "CPH:DANSKE": 110,
    "CPH:NDA-DK-volatility": 2,
    "EONIA": 0.006,
    "DKKLIBOR-1W": 0.00002,
}

class Equity:
    @classmethod
    def collect_data(cls, df, scenario):
        df["rf_value"] = None
        df.rf_value = df.rf.apply(scenario.get)
        return df

    @classmethod
    def price(cls, df):
        df["unit_price"] = df.rf_value
        df["price"] = df.unit_price * df.position
        return df

class VanillaCallOption:
    @classmethod
    def collect_data(cls, df, scenario):
        df["rf_value"] = None
        df["underlying_volatility_rf"] = df.rf.apply(lambda x:f"{x}-volatility")
        df["underlying_volatility"] = df.underlying_volatility_rf.apply(scenario.get)
        df.rf_value = df.rf.apply(scenario.get)
        df["interest_rate"] = None
        df.interest_rate = df.interest_rate_rf.apply(scenario.get)
        return df

    @classmethod
    def price(cls, df):
        S = df.rf_value # Spot
        K = df.strike

        # T: time to maturity
        T = df.maturity - df.day

        # r: interest rate
        r = df.interest_rate

        # sigma: volatility of underlying asset
        sigma = df.underlying_volatility

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        df["unit_price"] = S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(
            d2, 0.0, 1.0
        )
        df["price"] = df.unit_price * df.position
        return df

@command
def collect_data(df, scenario_name="scenario"):
    if type(scenario_name) == str:
        scen = eval(scenario_name)
    cdf = []
    for group, gdf in df.groupby("asset_type"):
        gdf["day"]=scen["DAY"]
        cdf.append(eval(group).collect_data(gdf, scen))
    return pd.concat(cdf)

@command
def add_price(df):
    cdf = []
    for group, gdf in df.groupby("asset_type"):
        gdf["day"]=scenario["DAY"]
        cdf.append(eval(group).price(gdf))
    return pd.concat(cdf)

evaluate_and_save("create_portfolio/collect_data/collected_data.xlsx")
evaluate_and_save("create_portfolio/collect_data/add_price/price1.xlsx")
evaluate_and_save("create_portfolio/collect_data-scenario2/add_price/price2.xlsx")