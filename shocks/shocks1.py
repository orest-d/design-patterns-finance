scenario = {
    "CPH:NDA-DK": 67.63,
    "CPH:DANSKE": 106.1,
    "CPH:NDA-DK-volatility": 1,
    "EONIA": -0.0049,
    "DKKLIBOR-1W": -0.00002,
}

# shock


def danske_100(scenario):
    scenario = {**scenario}
    scenario["CPH:DANSKE"] = 100.0
    return scenario


class Equity:
    def __init__(self, ticker):
        self.ticker = ticker

    def price(self, scenario):
        return scenario[self.ticker]


def shock_impact(scenario, asset, shock):
    return asset.price(shock(scenario)) - asset.price(scenario)


portfolio = Equity("CPH:DANSKE")

print("Portfolio price:", portfolio.price(scenario))
print("Shock impact:   ", shock_impact(scenario, portfolio, danske_100))
