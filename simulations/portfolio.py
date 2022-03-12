# Composite pattern - Option
import numpy as np
import scipy.stats as si
from config import *
import yaml


class Asset:
    def price(self, scenario, pricing_engine):
        raise NotImplementedError("Abstract asset does not have a price")

    def volatility(self, scenario, pricing_engine):
        raise NotImplementedError("Abstract asset does not have a volatility")

    @staticmethod
    def day(scenario):
        return scenario["DAY"]

    def clone(self):
        return self.from_dict(self.as_dict())

    def position(self, amount):
        return Position(amount, self.clone())

    def as_dict(self):
        return dict(asset_type=self.__class__.__name__)

    @classmethod
    def from_dict(cls, d):
        assert d["asset_type"] == cls.__class__.__name__
        return cls()

    def children(self):
        return []

    def descendants(self):
        for x in self.children():
            yield x
            for xx in x.descendants():
                yield xx

    def __str__(self):
        return self.__class__.__name__


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

    def clone(self):
        # return VanillaCallOption(self.strike, self.maturity, self.asset)  # Would not work in subclasses
        return self.__class__(self.strike, self.maturity, self.asset)

    def children(self):
        return [self.asset]

    def interest_rate(self, scenario):
        return scenario["EONIA"]

    def price(self, scenario, pricing_engine):
        spot = self.asset.price(scenario, pricing_engine)
        volatility = self.asset.volatility(scenario, pricing_engine)
        return pricing_engine.vanilla_call_option_price(
            strike=self.strike,
            time_to_maturity=self.maturity - self.day(scenario),
            spot_price=spot,
            volatility=volatility,
            interest_rate=self.interest_rate(scenario),
        )

    def volatility(self, scenario, pricing_engine):
        raise NotImplementedError("TBD")

    def as_dict(self):
        return dict(
            asset_type=self.__class__.__name__,
            strike=self.strike,
            asset=self.asset.as_dict(),
            maturity=self.maturity,
        )

    @classmethod
    def from_dict(cls, d):
        assert d["asset_type"] == "VanillaCallOption"
        asset_class = eval(d["asset"]["asset_type"])  # Interpreter
        asset = asset_class.from_dict(d["asset"])
        return cls(strike=d["strike"], maturity=d["maturity"], asset=asset)


class Equity(Asset):
    def __init__(self, ticker):
        self.ticker = ticker

    def call_option(self, strike, maturity):
        return VanillaCallOption(strike, maturity, self.clone())

    def clone(self):
        return Equity(self.ticker)

    def price(self, scenario, pricing_engine):
        return pricing_engine.equity_price(scenario, self.ticker)

    def volatility(self, scenario, pricing_engine):
        return pricing_engine.equity_volatility(scenario, self.ticker)

    def as_dict(self):
        return dict(
            asset_type=self.__class__.__name__,
            ticker=self.ticker,
        )

    @classmethod
    def from_dict(cls, d):
        assert d["asset_type"] == "Equity"
        return cls(d["ticker"])

    def __str__(self):
        return self.ticker


class Position(Asset):
    def __init__(self, amount, asset):
        self.amount = amount
        self.asset = asset

    def clone(self):
        return Position(self.amount, self.asset.clone())

    def price(self, scenario, pricing_engine):
        return self.amount * self.asset.price(scenario, pricing_engine)

    def volatility(self, scenario):
        return self.amount * self.asset.volatility(scenario, pricing_engine)

    def children(self):
        yield self.asset

    def as_dict(self):
        return dict(
            asset_type=self.__class__.__name__,
            asset=self.asset.as_dict(),
            amount=self.amount,
        )

    @classmethod
    def from_dict(cls, d):
        assert d["asset_type"] == "Position"
        asset_class = eval(d["asset"]["asset_type"])  # Interpreter
        asset = asset_class.from_dict(d["asset"])
        return cls(amount=d["amount"], asset=asset)

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

    def price(self, scenario, pricing_engine):
        return sum(x.price(scenario, pricing_engine) for x in self.assets)

    def volatility(self, scenario, pricing_engine):
        raise NotImplementedError("This is too complicated due to correlations")

    def children(self):
        return self.assets

    def as_dict(self):
        return dict(
            asset_type=self.__class__.__name__,
            assets=[x.as_dict() for x in self.assets],
        )

    @classmethod
    def from_dict(cls, d):
        assert d["asset_type"] == "Portfolio"
        assets = [eval(x["asset_type"]).from_dict(x) for x in d["assets"]]
        return cls(assets)


class VanillaCallOptionDK(VanillaCallOption):
    def interest_rate(self, scenario):
        return scenario["DKKLIBOR-1W"]


# Prototypes

NORDEA_TICK = "CPH:NDA-DK"
DANSKE_TICK = "CPH:DANSKE"
NORDEA = Equity(NORDEA_TICK)
DANSKE = Equity(DANSKE_TICK)


def default_portfolio():
    path = config()["portfolio"]
    print(f"Load default portfolio from {path}")
    with open(path) as f:
        x = yaml.load(f)
        return eval(x["asset_type"]).from_dict(x)


if __name__ == "__main__":
    import yaml

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
    with open("portfolio.yaml", "w") as f:
        yaml.dump(portfolio.as_dict(), f)

    scenario = {
        "DAY": 1,
        "CPH:NDA-DK": 67.63,
        "CPH:DANSKE": 106.1,
        "CPH:NDA-DK-volatility": 1,
        "EONIA": -0.0049,
        "DKKLIBOR-1W": -0.00002,
    }

    for x in portfolio.descendants():
        print(str(x))
    print("\n")
    for x in default_portfolio().descendants():
        print(str(x))
