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


class AbsoluteShock:
    def __init__(self, risk_factor, value):
        self.risk_factor = risk_factor
        self.value = value

    def __call__(self, scenario):
        scenario = {**scenario}
        scenario[self.risk_factor] = self.value
        return scenario


class RelativeShock:
    def __init__(self, risk_factor, value):
        self.risk_factor = risk_factor
        self.value = value

    def __call__(self, scenario):
        scenario = {**scenario}
        scenario[self.risk_factor] *= self.value
        return scenario


class Asset:
    pass


class Equity(Asset):
    def __init__(self, name):
        self.name = name

    def price(self, scenario):
        return scenario[self.name]


def shock_impact(scenario, asset, shock):
    return asset.price(shock(scenario)) - asset.price(scenario)


portfolio = Equity("CPH:DANSKE")

print("Portfolio price:", portfolio.price(scenario))
print("Shock impact 1: ", shock_impact(scenario, portfolio, danske_100))
print(
    "Shock impact 2: ",
    shock_impact(scenario, portfolio, AbsoluteShock("CPH:DANSKE", 105.0)),
)
print(
    "Shock impact 3: ",
    shock_impact(scenario, portfolio, RelativeShock("CPH:DANSKE", 1.0001)),
)


print(
    "Shock impact 4: ",
    shock_impact(scenario, portfolio, lambda s: {k: v * 0.95 for k, v in s.items()}),
)
