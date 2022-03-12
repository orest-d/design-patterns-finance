# Composite pattern - Option
import numpy as np
import scipy.stats as si


class PricingEngine:   # Bridge, Strategy
    default_equity_volatility = 1.0
    def equity_price(self, scenario, ticker):
        return scenario[ticker]
    def equity_volatility(self, scenario, ticker):
        return scenario.get(ticker+"_volatility", self.default_equity_volatility)
    def vanilla_call_option_price(self, strike, time_to_maturity, spot_price, volatility, interest_rate):
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
            return scenario["CPH:NDA-DK"]*106.1/67.63 + residual
        return scenario[ticker]


class Asset:
    def price(self, scenario, pricing_engine):
        raise NotImplementedError("Abstract asset does not have a price")

    def volatility(self, scenario, pricing_engine):
        raise NotImplementedError("Abstract asset does not have a volatility")

    @staticmethod
    def day(scenario):
        return scenario["DAY"]


class NullAsset(Asset):
    def price(self, scenario, pricing_engine):
        return 0.0

    def volatility(self, scenario, pricing_engine):
        return 0.0


class VanillaCallOption(Asset):
    def __init__(self, strike, maturity, asset):
        self.strike = strike
        self.asset = asset
        self.maturity = maturity

    def interest_rate(self, scenario):
        return scenario["EONIA"]

    def price(self, scenario, pricing_engine):
        spot = self.asset.price(scenario, pricing_engine)
        volatility = self.asset.volatility(scenario, pricing_engine)
        return pricing_engine.vanilla_call_option_price(
            strike = self.strike,
            time_to_maturity = self.maturity - self.day(scenario),
            spot_price = spot,
            volatility = volatility,
            interest_rate = self.interest_rate(scenario))

    def volatility(self, scenario, pricing_engine):
        raise NotImplementedError("TBD")


class Equity(Asset):
    def __init__(self, ticker):
        self.ticker = ticker

    def price(self, scenario, pricing_engine):
        return pricing_engine.equity_price(scenario, self.ticker)

    def volatility(self, scenario, pricing_engine):
        return pricing_engine.equity_volatility(scenario, self.ticker)


class Position(Asset):
    def __init__(self, amount, asset):
        self.amount = amount
        self.asset = asset

    def price(self, scenario, pricing_engine):
        return self.amount * self.asset.price(scenario, pricing_engine)

    def volatility(self, scenario):
        return self.amount * self.asset.volatility(scenario, pricing_engine)


class Portfolio(Asset):
    def __init__(self, assets=None):  # Don't use list as a default!
        self.assets = assets or []

    def price(self, scenario, pricing_engine):
        return sum(x.price(scenario, pricing_engine) for x in self.assets)

    def volatility(self, scenario, pricing_engine):
        raise NotImplementedError("This is too complicated due to correlations")


class VanillaCallOptionDK(VanillaCallOption):
    def interest_rate(self, scenario):
        return scenario["DKKLIBOR-1W"]


if __name__ == "__main__":
    portfolio = Portfolio(
        [
            Position(100, Equity("CPH:NDA-DK")),
            Position(10, Equity("CPH:DANSKE")),
            Position(1, VanillaCallOptionDK(70.0, 10, Equity("CPH:NDA-DK"))),
        ]
    )

    scenario = {
        "DAY": 1,
        "CPH:NDA-DK": 67.63,
        "CPH:DANSKE": 106.1,
        "CPH:NDA-DK-volatility": 1,
        "EONIA": -0.0049,
        "DKKLIBOR-1W": -0.00002,
    }
    pricing_engine = PricingEngine()

    print(portfolio.price(scenario, pricing_engine), "DKK")
    print(portfolio.price(scenario, PricingEngineWithProxyAndResidual()), "DKK")

#    print(VanillaCallOption(70.0, 10, Equity("CPH:NDA-DK")).price(scenario, pricing_engine))
#    print(VanillaCallOptionDK(70.0, 10, Equity("CPH:NDA-DK")).price(scenario, pricing_engine))
