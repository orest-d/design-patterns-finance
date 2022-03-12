# Composite pattern - Option
import numpy as np
import scipy.stats as si


class Asset:
    def price(self, scenario):
        raise NotImplementedError("Abstract asset does not have a price")

    def volatility(self, scenario):
        raise NotImplementedError("Abstract asset does not have a volatility")

    @staticmethod
    def day(scenario):
        return scenario["DAY"]


class NullAsset(Asset):
    def price(self, scenario):
        return 0.0

    def volatility(self, scenario):
        return 0.0


class VanillaCallOption(Asset):
    def __init__(self, strike, maturity, asset):
        self.strike = strike
        self.asset = asset
        self.maturity = maturity

    def interest_rate(self, scenario):
        return scenario["EONIA"]

    def price(self, scenario):
        # from https://aaronschlegel.me/black-scholes-formula-python.html

        # S: spot price
        S = self.asset.price(scenario)
        # K: strike price
        K = self.strike

        # T: time to maturity
        T = self.maturity - self.day(scenario)

        # r: interest rate
        r = self.interest_rate(scenario)

        # sigma: volatility of underlying asset
        sigma = self.asset.volatility(scenario)

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        return S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(
            d2, 0.0, 1.0
        )

    def volatility(self, scenario):
        # S: spot price
        S = self.asset(scenario)
        # K: strike price
        K = self.strike

        # T: time to maturity
        T = self.maturity - self.day(scenario)

        # r: interest rate
        r = self.interest_rate(scenario)

        # sigma: volatility of underlying asset
        sigma = self.asset.volatility(scenario)

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        vega = (
            1
            / np.sqrt(2 * np.pi)
            * S
            * np.exp(-q * T)
            * np.exp(-(d1 ** 2) * 0.5)
            * np.sqrt(T)
        )

        return vega


class Equity(Asset):
    def __init__(self, name):
        self.name = name

    def price(self, scenario):
        return scenario[self.name]

    def volatility(self, scenario):
        return scenario[self.name + "-volatility"]


class Position(Asset):
    def __init__(self, amount, asset):
        self.amount = amount
        self.asset = asset

    def price(self, scenario):
        return self.amount * self.asset.price(scenario)

    def volatility(self, scenario):
        return self.amount * self.asset.volatility(scenario)


class Portfolio(Asset):
    def __init__(self, assets=None):  # Don't use list as a default!
        self.assets = assets or []

    def price(self, scenario):
        return sum(x.price(scenario) for x in self.assets)

    def volatility(self, scenario):
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

    print(portfolio.price(scenario), "DKK")

    print(VanillaCallOption(70.0, 10, Equity("CPH:NDA-DK")).price(scenario))
    print(VanillaCallOptionDK(70.0, 10, Equity("CPH:NDA-DK")).price(scenario))
