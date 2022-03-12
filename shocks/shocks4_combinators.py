scenario = {
    "CPH:NDA-DK": 67.63,
    "CPH:DANSKE": 106.1,
    "CPH:NDA-DK-volatility": 1,
    "EONIA": -0.0049,
    "DKKLIBOR-1W": -0.00002,
}

# shock


class ShockMixin:  # Mixin, can be further extended
    def __add__(self, shock):
        return CombinedShock(self, shock)

    def __mul__(self, value):
        return RelativelyScaledShock(value, self)

    def __rmul__(self, value):
        return RelativelyScaledShock(value, self)


class ShockProxy(ShockMixin):  # Proxy
    def __init__(self, shock):
        self.shock = shock

    def __call__(self, scenario):
        return self.shock(scenario)


def rich_shock(f):
    return ShockProxy(f)


@rich_shock  # Python decorator
def danske_100(scenario):
    scenario = {**scenario}
    scenario["CPH:DANSKE"] = 100.0
    return scenario


class AbsoluteShock(ShockMixin):
    def __init__(self, risk_factor, value):
        self.risk_factor = risk_factor
        self.value = value

    def __call__(self, scenario):
        scenario = {**scenario}
        scenario[self.risk_factor] = self.value
        return scenario


class RelativeShock(ShockMixin):
    def __init__(self, risk_factor, value):
        self.risk_factor = risk_factor
        self.value = value

    def __call__(self, scenario):
        scenario = {**scenario}
        scenario[self.risk_factor] *= self.value
        return scenario


class RelativelyScaledShock:  # Another proxy
    def __init__(self, scaling_factor, shock):
        self.scaling_factor = scaling_factor
        self.shock = shock

    def __call__(self, scenario):
        shocked_scenario = self.shock(scenario)
        return {
            key: scenario[key]
            + self.scaling_factor * (shocked_scenario[key] - scenario[key])
            for key in scenario.keys()
        }


class CombinedShock:  # Combinator
    def __init__(self, shock1, shock2):
        self.shock1 = shock1
        self.shock2 = shock2

    def __call__(self, scenario):
        scenario = self.shock1(scenario)
        scenario = self.shock2(scenario)
        return scenario


class ScenarioShock(ShockMixin):  # Adapter
    def __init__(self, scenario):
        self.scenario = scenario

    def __call__(self, scenario):
        scenario = {**scenario}
        scenario.update(self.scenario)
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
print(
    "Shock impact 1: ", shock_impact(scenario, portfolio, danske_100)
)  # simple function works
print(
    "Shock impact 1a: ", shock_impact(scenario, portfolio, danske_100 * 2)
)  # decorated function enhanced by combinators
print(
    "Shock impact 2: ",
    shock_impact(scenario, portfolio, AbsoluteShock("CPH:DANSKE", 105.0)),
)  # callable object
print(
    "Shock impact 2a: ",
    shock_impact(scenario, portfolio, ScenarioShock({"CPH:DANSKE": 105.0})),
)  # adapter scenario -> shock
print(
    "Shock impact 3: ",
    shock_impact(scenario, portfolio, RelativeShock("CPH:DANSKE", 1.0001)),
)  # callable object
print(
    "Shock impact 3a: ",
    shock_impact(
        scenario, portfolio, danske_100 + 2 * RelativeShock("CPH:DANSKE", 1.0001)
    ),
)  # complex expression


print(
    "Shock impact 4: ",
    shock_impact(scenario, portfolio, lambda s: {k: v * 0.95 for k, v in s.items()}),
)  # simple lambda function
print(
    "Shock impact 4a: ",
    shock_impact(
        scenario,
        portfolio,
        rich_shock(lambda s: {k: v * 0.95 for k, v in s.items()}) * 2,
    ),
)  # decorated lambda function
