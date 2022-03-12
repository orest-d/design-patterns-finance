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

    def clone(self):
        raise NotImplementedError("Abstract asset clone not implemented")

    def position(self, amount):
        return Position(amount, self.clone())

    def children(self):
        return []

    def descendants(self):
        for x in self.children():
            yield x
            for xx in x.descendants():
                yield xx

    def __str__(self):
        return self.__class__.__name__


class VanillaCallOption(Asset):
    def __init__(self, strike, maturity, asset):
        self.strike = strike
        self.asset = asset
        self.maturity = maturity

    def clone(self):
        # return VanillaCallOption(self.strike, self.maturity, self.asset)  # Would not work in subclasses
        return self.__class__(self.strike, self.maturity, self.asset)

    def children(self):
        return [self.asset]

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

    def call_option(self, strike, maturity):
        return VanillaCallOption(strike, maturity, self.clone())

    def clone(self):
        return Equity(self.name)

    def price(self, scenario):
        return scenario[self.name]

    def volatility(self, scenario):
        return scenario[self.name + "-volatility"]

    def __str__(self):
        return self.name


class Position(Asset):
    def __init__(self, amount, asset):
        self.amount = amount
        self.asset = asset

    def clone(self):
        return Position(self.amount, self.asset.clone())

    def price(self, scenario):
        return self.amount * self.asset.price(scenario)

    def volatility(self, scenario):
        return self.amount * self.asset.volatility(scenario)

    def children(self):
        yield self.asset

    def __str__(self):
        return f"{self.amount} {self.asset}"


class Portfolio(Asset):
    def __init__(self, assets=None):  # Don't use list as a default!
        self.assets = assets or []

    def with_asset(self, asset):  # builder
        self.assets.append(asset)
        return self

    def equity_position(self, amount, name):  # builder
        return self.with_asset(Equity(name).position(amount))

    def clone(self):
        return Portfolio([x.clone() for x in self.assets])

    def price(self, scenario):
        return sum(x.price(scenario) for x in self.assets)

    def volatility(self, scenario):
        raise NotImplementedError("This is too complicated due to correlations")

    def children(self):
        return self.assets


class VanillaCallOptionDK(VanillaCallOption):
    def interest_rate(self, scenario):
        return scenario["DKKLIBOR-1W"]


# Prototypes

NORDEA_TICK = "CPH:NDA-DK"
DANSKE_TICK = "CPH:DANSKE"
NORDEA = Equity(NORDEA_TICK)
DANSKE = Equity(DANSKE_TICK)


if __name__ == "__main__":
    portfolio = Portfolio(
        [
            NORDEA.position(100.0),
            DANSKE.position(10.0),
            NORDEA.call_option(70.0, 10.0),
        ]
    )

    portfolio = (
        Portfolio()
        .equity_position(100.0, NORDEA_TICK)
        .equity_position(10.0, DANSKE_TICK)
        .with_asset(NORDEA.call_option(strike=70.0, maturity=10.0))
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

    for x in portfolio.descendants():
        print(str(x))
