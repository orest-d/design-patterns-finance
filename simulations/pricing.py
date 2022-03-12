# Composite pattern - Option
import numpy as np
import scipy.stats as si
from config import *


class PricingEngine:  # Bridge, Strategy
    default_equity_volatility = 1.0

    def equity_price(self, scenario, ticker):
        return scenario[ticker]

    def equity_volatility(self, scenario, ticker):
        return scenario.get(ticker + "_volatility", self.default_equity_volatility)

    def vanilla_call_option_price(
        self, strike, time_to_maturity, spot_price, volatility, interest_rate
    ):
        # from https://aaronschlegel.me/black-scholes-formula-python.html

        # S: spot price
        S = spot_price
        # K: strike price
        K = strike

        # T: time to maturity
        T = time_to_maturity

        # r: interest rate
        r = interest_rate

        # sigma: volatility of underlying asset
        sigma = volatility

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        return S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(
            d2, 0.0, 1.0
        )


class PricingEngineWithProxyAndResidual(PricingEngine):
    def equity_price(self, scenario, ticker):
        if ticker == "CPH:DANSKE":
            residual = np.random.normal(scale=2.123)
            return scenario["CPH:NDA-DK"] * 106.1 / 67.63 + residual
        return scenario[ticker]


def default_pricing_engine():
    return eval(config()["pricing_engine"])()
