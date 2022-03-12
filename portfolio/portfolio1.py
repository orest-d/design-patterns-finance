# Composite pattern

import re


class Asset:
    def price(self, scenario):
        raise NotImplementedError("Abstract asset does not have a price")


class Equity(Asset):
    def __init__(self, name):
        self.name = name

    def price(self, scenario):
        return scenario[self.name]


class Position(Asset):
    def __init__(self, amount, asset):
        self.amount = amount
        self.asset = asset

    def price(self, scenario):
        return self.amount * self.asset.price(scenario)


class Portfolio(Asset):
    def __init__(self, assets=None):  # Don't use list as a default!
        self.assets = assets or []

    def price(self, scenario):
        return sum(x.price(scenario) for x in self.assets)


if __name__ == "__main__":
    portfolio = Portfolio(
        [
            Position(100, Equity("CPH:NDA-DK")),
            Position(10, Equity("CPH:DANSKE")),
        ]
    )

    scenario = {"CPH:NDA-DK": 67.63, "CPH:DANSKE": 106.1}

    print(portfolio.price(scenario), "DKK")
